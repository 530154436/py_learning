# /usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib

def test_md5():
    '''
    计算出一个字符串的MD5值
    :return:
    '''
    md5 = hashlib.md5()
    print(md5)
    md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
    print(md5)
    print(md5.hexdigest())

    # 如果数据量很大，可以分块多次调用update()，最后计算的结果是一样的：
    md5 = hashlib.md5()
    md5.update('how to use md5 in '.encode('utf-8'))
    md5.update('python hashlib?'.encode('utf-8'))
    print(md5.hexdigest())

def test_sha1():
    sha1 = hashlib.sha1()
    sha1.update('how to use md5 in '.encode('utf-8'))
    sha1.update('python hashlib?'.encode('utf-8'))
    print(sha1.hexdigest())

db = {}

def get_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()

def login(user, password):
    print('login:', user, get_md5(password + user + 'the-Salt'))
    if user in db.keys() and get_md5(password + user + 'the-Salt') == db[user]:
        return 'Hello',user
    return 'Login Error'

def register(user, password):
    db[user]= get_md5(password + user + 'the-Salt')
    print('register:',user, db[user])

def exercise():
    register('michael', '123456')
    print(login('michael', '123'))
    print(login('michael', '123456'))


if __name__ == '__main__':
    test_md5()
    test_sha1()
    exercise()