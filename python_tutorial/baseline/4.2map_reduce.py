#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

def f(x):
	return x**2

def add(x, y):
	return x + y

def fn(x, y):
	return x * 10 + y

def char2num(s):
	return {'0':0, '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7, '8':8,'9':9, '.':-1}[s]
 
# 字符转为整型
def char2int(s):
	return reduce(fn, map(char2num, s))

# lambda
def char2int(s):
	return reduce(lambda x, y : x * 10 + y, map(char2num, s))

# 练习1: 把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字
def normalize(name):
	res = name[0].upper() + name[1:].lower()
	return res

# 练习2：接受一个list并利用reduce()求积
def prod(L):
	def pro(x, y):
		return x * y
	return reduce(pro, L)

# 练习3：利用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456
def str2float1(s):
	
	def char2num(s):
		return {'0':0, '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7, '8':8,'9':9,}[s]

	def fn(x, y):
		return x * 10 + y

	def char2int(s):
		return reduce(fn, map(char2num, s))
	
	i = s.index('.')
	x = char2int(s[0:i])
	y = char2int(s[i+1:])
	return x + 0.1 ** len(s[i+1:]) * y

x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
m = list(map(f, x))
sm = list(map(str, x))

print(m)
print(sm)

print(reduce(add, x))
print(reduce(fn, x))

print(reduce(fn, map(char2num, '1234')))
print(char2int('12323124209082'))

L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))

print('str2float(\'123.456312\') =', str2float1('123.456312'))
print(str2float2('120.0034'))


