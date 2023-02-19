#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from neo4j import GraphDatabase,unit_of_work

class Neo4jUtil(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def dict2str(self, data: dict):
        ''' 将字典转换为字符串 (注意字符串类型的数据格式) '''
        kv_list = []
        for k, v in data.items():
            if isinstance(v, str):
                kv = f'{k}: \'{v}\''
            else:
                kv = f'{k}: {v}'
            kv_list.append(kv)
        kv_str = '{%s}' % ', '.join(kv_list)
        return kv_str

    def dict2setStr(self, node: str, data: dict):
        ''' 将字典转换为 CQL-Set 的格式 '''
        kv_list = []
        for k, v in data.items():
            if isinstance(v, str):
                kv = r"""%s.%s='%s'""" % (node, k, v)
            else:
                kv = f'{node}.{k}={v}'
            kv_list.append(kv)
        kv_str = ', '.join(kv_list)
        return kv_str

    def __transaction(self, func, is_write_mode):
        '''
        事务
        :param func:            一个函数
        :param is_write_mode:   是否为写模式
        :return:
        '''
        # 官方推荐使用事务函数进行节点创建
        with self._driver.session() as session:
            # Caller for transactional unit of work
            if is_write_mode:
                return session.write_transaction(func)
            else:
                return session.read_transaction(func)

    def exec_cql(self, cql:str, is_write_mode:bool=False, parameters:dict=None, **kwparameters):
        '''
        直接执行cql语句
        :param cql:             cql 语句: 传参方式中指定参数格式(选其一) -> $参数名、{参数名}
        :param is_write_mode:   是否为写模式
        :param parameters:      字典: {参数名:值}
        :param kwparameters:    关键字参数: 参数名=值
        :return:
        '''
        return self.__transaction(
            lambda tx:tx.run(cql, parameters, **kwparameters).value(), is_write_mode)

    def createUniqueConstraint(self, label_name:str, field_name:str):
        '''
        创建唯一键约束(unique): 避免重复记录、强制执行数据完整性规则
        语法:
            CREATE CONSTRAINT ON (<label_name>) ASSERT <property_name> IS UNIQUE
        :param label_name:  标签名
        :param field_name:  字段名
        :return:
        '''
        def __addConstraint(tx):
            cql = f'CREATE CONSTRAINT ON ({label_name.lower()}:{label_name}) ' \
                  f'       ASSERT {label_name.lower()}.{field_name} IS UNIQUE'
            return tx.run(cql)
        return self.__transaction(__addConstraint, is_write_mode=True)

    def createNode(self, label_name, properties:dict=None, timeout=10):
        '''
        创建节点: 无属性或具有一些属性（键值对）
        语法:
            CREATE ( <node-name>:<label-name>)
            CREATE ( <node-name>:<label-name> { <Property1-name>:<Property1-Value>} )
        :param label_name:  标签名
        :param properties:  属性值
        :param timeout:     超时(单位/秒)
        :return None或neo4j.Record对象
        '''
        @unit_of_work(timeout=timeout)
        def __addNode(tx):
            cql = f'CREATE (a:{label_name})'
            if properties:
                # 构造属性值的cql
                # p2str = '{%s}' % ', '.join(['{}: ${}'.format(key, key) for key in properties.keys()])
                # cql = f'CREATE (a:{label_name} {p2str})\n' \
                #       f'RETURN id(a),a'

                data = {'data':properties}

                # 唯一约束，保证user_id唯一
                cql = 'CREATE (a:%s {data})\n' \
                      'RETURN id(a),a' % (label_name)
                return tx.run(cql, data).single()
            return tx.run(cql).single()
        return self.__transaction(__addNode, is_write_mode=True)

    def mergeOnCreateNode(self, merge_condition:dict, label_name:str, properties:dict, timeout=10):
        '''
        合并节点：(1) 不存在则创建
                (2) 存在则更新属性
        :param merge_condition: 匹配节点的条件(类似主键)
        :param label_name:      标签名
        :param properties:      节点属性
        :param timeout:         超时时间
        :return:
        '''
        @unit_of_work(timeout=timeout)
        def __createOrMatchNode(tx):
            node_name = label_name.lower()

            # 拼接MERGE的匹配条件
            merge_condition_str = self.dict2str(merge_condition)

            # 拼接更新语句
            set_str = self.dict2setStr(node_name, properties)

            cql = f'MERGE ({node_name}:{label_name} {merge_condition_str})\n' \
                  f'ON CREATE SET {set_str}\n' \
                  f'ON MATCH SET {set_str}\n' \
                  f'RETURN {node_name}'
            return tx.run(cql).single()

        if merge_condition and label_name and properties:
            return self.__transaction(__createOrMatchNode, is_write_mode=True)
        else:
            return None

    def createRelationshipsBtwTwoNodes(self, node1:tuple, node2:tuple, relationship):
        '''
        创建两个节点之间的关系  >>  https://neo4j.com/docs/cypher-manual/current/clauses/create/
        :param node1:        节点1 (label_name_1, 'user_id', '1110')
        :param node2:        节点2 (label_name_2, 'user_id', '1100')
        :param label_name:   标签名
        :param relationship: 关系
        :return:
        '''
        res_properties =r"""{name: a.%s + '-%s->' + b.%s}""" % (node1[1], relationship, node2[1])
        condition = r"""a.%s = '%s' AND b.%s = '%s'""" % (node1[1], node1[2], node2[1], node2[2])

        def __addRelationship(tx):
            cql = f'MATCH (a:{node1[0]}),(b:{node2[0]})\n' \
                  f'WHERE {condition}\n' \
                  f'CREATE (a)-[r:{relationship} {res_properties}]->(b)\n' \
                  f'RETURN type(r), r.name'
            return tx.run(cql).single()

        return self.__transaction(__addRelationship, is_write_mode=True)

    def deleteNodesByLabel(self, label_name:str, deleteRelationship=False):
        '''
        删除标签名下的所有节点和边
        :param label_name:          标签名
        :param deleteRelationship   是否删除边
        :return:
        '''
        cql = f'MATCH ({label_name.lower()}: {label_name}) DELETE {label_name.lower()}'
        if deleteRelationship:
            cql = f'MATCH ({label_name.lower()}: {label_name}) DETACH DELETE {label_name.lower()}'
        return self.exec_cql(cql, is_write_mode=True)

    def deleteUniqueConstraint(self, label_name:str, field_name:str):
        '''
        删除键约束  >> https://neo4j.com/docs/cypher-manual/current/schema/constraints/
        :param label_name:  标签名
        :param field_name:  字段名
        '''
        cql = f'DROP CONSTRAINT ON ({label_name.lower()}:{label_name}) ' \
              f'     ASSERT {label_name.lower()}.{field_name} IS UNIQUE'
        return self.exec_cql(cql, is_write_mode=True)

    def deleteLabel(self, label_name:str):
        '''
        删除标签  >> https://neo4j.com/docs/cypher-manual/current/clauses/remove/
        :param label_name:
        :return:
        '''
        cql = f'MATCH (u:{label_name}) REMOVE u:{label_name}'
        return self.exec_cql(cql, is_write_mode=True)