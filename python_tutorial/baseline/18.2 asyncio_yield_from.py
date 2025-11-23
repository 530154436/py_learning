# /usr/bin/env python3
# -*- coding:utf-8 -*-
def g1():
    yield range(5)

def g2():
    yield from range(5)
    # yield from iterable本质上等于for item in iterable: yield item的缩写版
    # yield from 后面必须跟 iterable 对象(可以是生成器，迭代器)

int1 = g1()
int2 = g2()

for x in int1:
    print(x)

for x in int2:
    print(x)

def fab(max):
    n,a,b = 0, 0, 1
    while n < max:
        yield b
        a,b = b, a+b
        n = n + 1

def f_warpper(fun_iterable):
    print('start')
    for item in fun_iterable:
        yield item
    print('end')

def f_warpper2(fun_iterable):
    print('start')
    yield from fun_iterable
    print('end')

wrap1 = f_warpper(fab(5))
for i in wrap1:
    print(i, end=' ')


wrap2 = f_warpper2(fab(5))
for i in wrap2:
    print(i, end=' ')