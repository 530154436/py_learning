# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import pymysql

from app.apis.hotel_rec import settings
from app.apis.hotel_rec.util.database import DataBase


class MySql(DataBase):
    def __init__(self, host, port, user, password, dbName):
        super(MySql, self).__init__(host, port, user, password)
        self._dbName = dbName
        self._db = self._init()

    def getCon(self):
        return self._db

    def _init(self, charset='utf8mb4', cursorClass=None): # connection
        if not cursorClass:
            cursorClass=pymysql.cursors.SSCursor
        connect  = pymysql.connect(host=self._host,
                                   user=self._user,
                                   port=self._port,
                                   password=self._password,
                                   db=self._dbName,
                                   charset=charset,
                                   cursorclass=cursorClass)
        return connect

    def query(self, sql, cursorClass=None):
        '''
        封装查询接口
        :param sql:         SQL查询语句
        :param cursorClass: 游标类型（默认流式游标）
        :return: 游标
        '''
        if self._db is None:
            self._init()
        if cursorClass is None:
            cursorClass=pymysql.cursors.SSCursor
        cursor = cursorClass(self._db)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        finally:
            return cursor

if __name__ == '__main__':
    db = MySql(host=settings.MS_HOST,
               port=settings.MS_PORT,
               user=settings.MS_USER,
               password=settings.MS_PASSWORD,
               dbName=settings.MS_DB_HOTEL)
    print(db)