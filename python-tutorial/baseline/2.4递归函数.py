#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#计算阶乘
def fac(n):
	if n==1:
		return n
	return n * fac(n-1)

def fact(n):
	return fact_iter(n, 1)

def fact_iter(num, product):
	if num == 1:
		return product
	return fact_iter(num - 1, num * product)

#汉诺塔的移动
def move(n, a, b, c):
	if n==1:
		print(a,'-->',c) 
	else:
		move(n-1, a, c, b)
		move(1, a, b, c)
		move(n-1, b, a, c)


print(fac(5))
print(fact_iter(5, 1))
print(fact(5))
move(3, 'A', 'B', 'C')
