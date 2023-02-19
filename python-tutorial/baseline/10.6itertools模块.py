# /usr/bin/env python3
# -*- coding:utf-8 -*-

import itertools

def test_count():
    '''
    自然数序列
    :return:
    '''
    naturals = itertools.count(1)
    for i in naturals:
        print(i)

def test_cycle():
    '''
    把传入的一个序列无限重复下去
    '''
    cs = itertools.cycle('edward')
    for i in cs:
        print(i)

def test_repeat():
    '''
    repeat() 负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数
    :return:
    '''
    rt = itertools.repeat('edward',3)
    for i in rt:
        print(i)

def test_take_while():
    '''
    takewhile()等函数根据条件判断来截取出一个有限的序列
    :return:
    '''
    naturals = itertools.count(1)
    ns = itertools.takewhile(lambda x : x <= 10, naturals)
    print(list(ns))

def test_chain():
    '''
    可以把一组迭代对象串联起来，形成一个更大的迭代器：
    :return:
    '''
    for c in itertools.chain('ABC', 'XYZ'):
        print(c)

def test_groupby():
    '''
    把迭代器中相邻的重复元素挑出来放在一起
    :return:
    '''
    for key,group in itertools.groupby('AAABBBCCAAA'):
        print(key, list(group))

if __name__ == '__main__':
    # test_count()
    # test_cycle()
    # test_repeat()
    # test_take_while()
    # test_chain()
    test_groupby()
