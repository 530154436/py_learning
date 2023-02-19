#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@function:
"""
import pandas as pd
import data_loader
from utils.neo4j_util import Neo4jUtil

LABELS = {
    'Movie': 'mid',
    'Genre': 'gid',
    'Person': 'pid'
}

def create_cnstraint(conn):
    '''
    创建`键唯一`约束 -> 保证标签内唯一
    '''
    for label, _id in LABELS.items():
        conn.createUniqueConstraint(label, _id)

def clear(conn):
    '''
    谨慎使用：删除所有节点和关系
    '''
    for label, _id in LABELS.items():
        conn.deleteNodesByLabel(label, True)
        conn.deleteUniqueConstraint(label, _id)
        conn.deleteLabel(label)

def create_entity(conn, data: pd.DataFrame, label: str):
    '''
    创建实体节点
    '''
    for _row in data.to_dict(orient='records'):
        conn.createNode(label, properties=_row)

def create_relations(conn, data: pd.DataFrame,
                     label_from: str, label_to: str, relationship: str):
    '''
    创建实体关系
    '''
    _id_from = LABELS.get(label_from)
    _id_to = LABELS.get(label_to)
    for _row in data.to_dict(orient='records'):
        node1 = (label_from, _id_from, _row.get(_id_from))
        node2 = (label_to, _id_to, _row.get(_id_to))
        # print(node1, relationship, node2)
        conn.createRelationshipsBtwTwoNodes(node1, node2, relationship)


if __name__ == '__main__':
    conn = Neo4jUtil(uri='bolt://127.0.0.1/:7687', user='neo4j', password='7895123')

    # clear(conn)

    # 1. 创建约束
    create_cnstraint(conn)

    # 2. 创建实体: 电影、风格、演员
    create_entity(conn, data_loader.load_movie(), label='Movie')
    create_entity(conn, data_loader.load_genre(), label='Genre')
    create_entity(conn, data_loader.load_person(), label='Person')

    # 3. 创建关系
    create_relations(conn, data_loader.load_movie_to_genre(),
                     label_from='Movie', label_to='Genre', relationship='类别')
    create_relations(conn, data_loader.load_person_to_movie(),
                     label_from='Person', label_to='Movie', relationship='演员')

