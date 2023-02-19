#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/01/28
"""
import redis
import pymysql
from pymongo import MongoClient
from config import redis_host, redis_port, redis_pwd, \
                   mysql_host, mysql_port, mysql_pwd, mysql_user,\
                   connect_url

def get_redis_conn(db, host=redis_host, port=redis_port, pwd=redis_pwd, decode_responses=True):
    '''
    获取redis连接池连接
    :param db: 数据库
    :param decode_responses:
    :return:
    '''
    pool = redis.ConnectionPool(
        host=host, db=db, port=port, password=pwd, decode_responses=decode_responses)
    return redis.Redis(connection_pool=pool)

def get_mysql_conn(db, host=mysql_host, user=mysql_user, pwd=mysql_pwd,
                   port=mysql_port,  charset='utf8mb4', cursorClass=None):
    '''
    获取 mysql 连接池连接
    '''
    if not cursorClass:
        cursorClass=pymysql.cursors.SSCursor
    connect  = pymysql.connect(host=host,
                               user=user,
                               port=port,
                               password=pwd,
                               db=db,
                               charset=charset,
                               cursorclass=cursorClass)
    return connect

def get_mongo_conn(db, collection=None, connect_url=connect_url):
    '''
    获取 MongoDB 连接池连接
    '''
    client = MongoClient(connect_url, connect=False, maxPoolSize=50)
    if collection:
        return client[db][collection]
    else:
        return client[db]
