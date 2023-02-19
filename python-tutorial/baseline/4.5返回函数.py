#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def lazy_sum1(*args):
	def sum():
		s = 0
		for x in args:
			s += x
		return s
	return sum

def lazy_sum2(*args):
	global s
	s = 1
	def sum():
		global s
		for x in args:
			s += x
		return s
	return sum

def lazy_sum3(*args):
	s = 2
	def sum():
		nonlocal s
		for x in args:
			s += x
		return s
	return sum

f1 = lazy_sum1(1,2,4,5)
f2 = lazy_sum2(1,2,4,5)
f3 = lazy_sum3(1,2,4,5)
print(f1)
print(f1())
print(f2())
print(f3())

def count():
	fs = []
	for i in range(1,4):
		def f():
			return i*i
		fs.append(f)
	return fs

for f in count():
	print(f())

def count():
	def f(j):
		def g():
			return j*j
		return g
		
	fs = []
	for i in range(1,4):
		fs.append(f(i))
	return fs

for f in count():
	print(f())



