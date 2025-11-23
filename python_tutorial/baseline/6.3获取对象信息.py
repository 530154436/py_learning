#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import types

type(123)
type('str')
type(123) == type(456)
type(123) == int
type('123') == type('sdfad')

def fn():
	pass

type(fn) == types.FunctionType
type(abs) == types.BuiltinFunctionType
type(lambda x:x) == types.LambdaType
type((x for x in range(10))) == types.GeneratorType

isinstance([1,2,3], (list, tuple))

dir('12213')
'asdf'.__len__()

class MyDog(object):
	def __len__(self):
		return 100
len(MyDog())

class MyObject(object):
	def __init__(self):
		self.x = 9
	def power(self):
		return self.x * self.x
obj = MyObject()
hasattr(obj, 'x')
hasattr(obj, 'y')
setattr(obj, 'y', 19)
hasattr(obj, 'y')
getattr(obj, 'y')
getattr(obj, 'power')




