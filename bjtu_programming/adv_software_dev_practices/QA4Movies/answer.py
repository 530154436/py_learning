#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@function:
"""
from utils.neo4j_util import Neo4jUtil


class QAProcessor(object):

    conn = Neo4jUtil(uri='bolt://127.0.0.1/:7687', user='neo4j', password='7895123')

    @classmethod
    def get_actor_act_movies(cls, name):
        """ 返回演员饰演的电影列表 """
        cql = r"""
            MATCH(n:Person)-[]->(m:Movie) 
            WHERE n.name='%s'
            RETURN m.title
        """ % (name)
        print(cql)
        records = []
        for record in cls.conn.exec_cql(cql, is_write_mode=False):
            records.append(record)
        return records

    @classmethod
    def get_actor_act_movie_genre(cls, name):
        """ 返回演员饰演的电影类型 """
        cql = r"""
            MATCH(n:Person)-[]->(m:Movie)-[]->(g:Genre)
            WHERE n.name='%s'
            RETURN DISTINCT g.gname
        """ % (name)
        print(cql)
        records = []
        for record in cls.conn.exec_cql(cql, is_write_mode=False):
            records.append(record)
        return records

    @classmethod
    def get_actor_common_movies(cls, actor1, actor2):
        """ 返回两个演员共同饰演的电影列表"""
        cql = r"""
            MATCH(p1:Person)-[]->(m:Movie)<-[]-(p2:Person)
            WHERE p1.name='%s' AND p2.name='%s'
            RETURN DISTINCT m.title
        """ % (actor1, actor2)
        print(cql)
        records = []
        for record in cls.conn.exec_cql(cql, is_write_mode=False):
            records.append(record)
        return records

    @classmethod
    def get_movie_acotr_list(cls, name):
        """ 返回电影的演员列表 """
        cql = r"""
            MATCH(n:Person)-[r:`演员`]->(m:Movie) 
            WHERE m.title='%s' 
            RETURN n.name
        """ % (name)
        print(cql)
        records = []
        for record in cls.conn.exec_cql(cql, is_write_mode=False):
            records.append(record)
        return records

    @classmethod
    def get_movie_release_date(cls, name):
        """ 返回电影的上映日期 """
        cql = r"""
            MATCH(m:Movie) 
            WHERE m.title='%s' 
            RETURN m.releasedate
        """ % (name)
        print(cql)
        return cls.conn.exec_cql(cql, is_write_mode=False)[0]

    @classmethod
    def get_movie_genre(cls, name):
        """ 返回电影的风格 """
        cql = r"""
            MATCH(m:Movie) -[r:`类别`]->(g:Genre) 
            WHERE m.title='%s' 
            RETURN g.gname
        """ % (name)
        print(cql)
        records = []
        for record in cls.conn.exec_cql(cql, is_write_mode=False):
            records.append(record)
        return records

    @classmethod
    def get_movie_evaluation(cls, name):
        """ 返回电影的评分 """
        cql = r"""
            MATCH(m:Movie)
            WHERE m.title='%s' 
            RETURN m.rating
        """ % (name)
        print(cql)
        return cls.conn.exec_cql(cql, is_write_mode=False)[0]

    @classmethod
    def template_1(cls, name):
        """ 问题模板1：xx演员演了哪些电影？ """
        movies = cls.get_actor_act_movies(name)
        rsp = f'{name}演过的电影有{"、".join(movies)}'
        return rsp

    @classmethod
    def template_2(cls, name):
        """问题模板2：xx电影的演员有哪些？"""
        return cls.get_movie_acotr_list(name)

    @classmethod
    def template_3(cls, name):
        """问题模板3：xx电影是什么风格？"""
        return cls.get_movie_genre(name)

    @classmethod
    def template_4(cls, name):
        """问题模板4：xx电影评分是多少？"""
        return cls.get_movie_evaluation(name)

    @classmethod
    def template_5(cls, name):
        """问题模板5：xx演员演过哪些类型的电影？"""
        return cls.get_actor_act_movie_genre(name)

    @classmethod
    def template_6(cls, name):
        """问题模板6：xx电影的上映时间是？"""
        return cls.get_movie_release_date(name)

    @classmethod
    def template_7(cls, actor1, actor2):
        """问题模板7：A演员和B演员合作过哪些电影？"""
        return cls.get_actor_common_movies(actor1, actor2)

    @classmethod
    def template_8(cls, name):
        """问题模板8：xx演员出演过多少部电影？"""
        return len(cls.get_actor_act_movies(name))


if __name__ == '__main__':
    print(QAProcessor.template_1('周润发'))
    print(QAProcessor.template_2('卧虎藏龙'))
    print(QAProcessor.template_3('卧虎藏龙'))
    print(QAProcessor.template_4('卧虎藏龙'))
    print(QAProcessor.template_5('周润发'))
    print(QAProcessor.template_6('卧虎藏龙'))
    print(QAProcessor.template_7('周润发', '章子怡'))
    print(QAProcessor.template_8('周润发'))
