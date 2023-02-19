# !/usr/bin/env python3
# -*- coding : utf-8 -*-
from pymongo import MongoClient

from app.apis.hotel_rec import settings
from app.apis.hotel_rec.util.database import DataBase


class MonGoDB(DataBase):
    ''' 封装mongodb接口 '''

    def __init__(self, host, port, user, password, authSource, authMechanism):
        super(MonGoDB, self).__init__(host, port, user, password)
        self._authSource = authSource
        self._authMechanism = authMechanism
        self._db = self._init()

    def _init(self):
        client  =  MongoClient(host=self._host,
                               port=self._port,
                               username=self._user,
                               password=self._password,
                               authSource=self._authSource,
                               authMechanism=self._authMechanism)
        return client

    def query(self, dbName, collection, query, fields=None, no_cursor_timeout=True):
        '''
        查询功能
        :param dbName:           数据库名
        :param collection:       集合名
        :param query:            查询语句
        :param fields:           需要返回的字段，default: 返回全部字段
        :param no_cursor_timeout:设置游标是否超时断开
        :return: 游标
        '''
        if self._db is None:
            self._init()


        cursor = self._db[dbName][collection]\
            .find(query, fields, no_cursor_timeout=no_cursor_timeout)
        return cursor

if __name__ == '__main__':
    client = MonGoDB(host=settings.MDB_HOST,
                     port=settings.MDB_PORT,
                     user=settings.MDB_USERNAME,
                     password=settings.MDB_PASSWORD,
                     authSource=settings.MDB_AUTH_SOURCE,
                     authMechanism=settings.MDB_AUTH_MECHANISM)
    print(client)
    client.close()
    print(client)