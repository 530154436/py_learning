#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

list01 = list(range(1,11))
list02 = [ x*x for x in list01]
list03 = [ x*x for x in list01 if x%2==0]

list04 = [ m+n for m in 'ABC' for n in 'XYZ']

list05 = [ d for d in os.listdir('.')]

print(list01)
print(list02)
print(list03)
print(list04)
print(list05)

dic01 = {'x':'a','y':'b','z':'c'}
list06 = [ k+'='+v for k,v in dic01.items()]

print(dic01)

x = 'abcdefg'
y= 12345
a = isinstance(x, str)
b = isinstance(y, str)

print(a)
print(b)

L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [ s.lower() for s in L1 if isinstance(s,str) ]

print(L2)


