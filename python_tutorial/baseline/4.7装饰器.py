#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

def log(func):
	def wrapper(*args, **kw):
		print('call %s():' % func.__name__)
		return func(*args, **kw)
	return wrapper

@ log
def now():
	print('2015-3-25')

f = now 
f()
print(now.__name__)
print(f.__name__)

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def  wrapper(*args, **kw):
			print('%s %s():' % (text, func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator

@ log('execute')
def now():
	print('2015-3-25')

now()
print(now.__name__)

#练习1
def log(func):
	def decorator(*args, **kw):
		print('begin call')
		func()
		print('end call')
	return decorator

#练习2
def log(text):
	def decorator01(func):
		return func

	def decorator02(func):
		def wrapper(*args, **kw):
			print('接收到text参数: %s' % text)
			return func(*args, **kw)
		return wrapper

	if isinstance(text, str):
		return decorator02
	else:
		return decorator01(text)

@ log
def func01():
	print('calling func')

@ log('execute')
def func02():
	print('calling execute func')

func02()
func01()


