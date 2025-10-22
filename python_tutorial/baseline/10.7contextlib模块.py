# /usr/bin/env python3
# -*- coding:utf-8 -*-
from contextlib import contextmanager
from urllib.request import urlopen

class Query1(object):
    '''
    上下文管理协议（Context Management Protocol）：包含方法 __enter__() 和 __exit__()
    '''
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('begin')
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)

class Query2(object):

    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...' % self.name)

@contextmanager
def create_query(name):
    print('begin')
    q = Query2(name)
    yield q
    print('End')

@contextmanager
def tag(name):
    '''
    代码的执行顺序是：
        1. with语句首先执行yield之前的语句，因此打印出<h1>；
        2. yield调用会执行with语句内部的所有语句，因此打印出hello和world；
        3. 最后执行yield之后的语句，打印出</h1>。
    '''
    print('<%s>' % name)
    yield
    print('</%s>' % name)

with create_query('Bob') as q:
    q.query()

with tag('h1'):
    print('Hello')
    print('World')

@contextmanager
def closing(thing):
    '''
    它的作用就是把任意对象变为上下文对象，并支持with语句。
    :param thing:
    :return:
    '''
    try:
        yield thing
    finally:
        thing.close()

with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line.decode('utf-8').strip())





