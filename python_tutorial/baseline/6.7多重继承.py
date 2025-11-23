#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect

class Animal(object):
	pass

class Mammal(Animal):
	pass

class Bird(Animal):
	pass

class RunnableMixIn(object):
	def run(self):
		print('Running ...')

class FlyableMixIn(object):
	def fly(self):
		print('Flying ...')

class Dog(Mammal, RunnableMixIn):
	pass

class Bat(Mammal, FlyableMixIn):
	pass

class Parrot(Bird, FlyableMixIn):
	pass

class Ostrich(Bird, RunnableMixIn):
	pass

# http://jbcdn2.b0.upaiyun.com/2016/07/67b3fe6d97b5882482cc0ca65cec6154.jpg
#python2 存在新式和经典类
#1. 如果是经典类MRO为DFS（深度优先搜索（子节点顺序：从左到右））。

class D(object):   # 继承于object
    def __init__(self):
        print("这是新式类")
 
class D(): # 经典类
    pass

#Python3开始就只存在新式类
#如果是新式类MRO为BFS（广度优先搜索（子节点顺序：从左到右））。
class D():
    pass
 
class C(D):
    pass
 
class B(D):
    pass
 
class A(B, C):
    pass
 
if __name__ == '__main__':
	#pyhon3 (<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.D'>, <class 'object'>)
    #python2 (<class __main__.A at 0x10070bef0>, <class __main__.B at 0x10070be88>, <class __main__.D at 0x10070bdb8>, <class __main__.C at 0x10070be20>)
    print(inspect.getmro(A))



