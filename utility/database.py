# !/usr/bin/env python3
# -*- coding : utf-8 -*-
class DataBase(object):
    def __init__(self, host, port, user, password):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._db = None

    def _init(self):
        '''
        初始化客户端
        :return:
        '''
        pass

    def close(self):
        '''
        关闭连接
        :return:
        '''
        try:
            if not self._db:
                self._db.close()
                print('连接已关闭.')
        except Exception as e:
            print(e)