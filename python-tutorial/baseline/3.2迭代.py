#!/usr/bin/env python3
# -*- coding: utf-8 -*-

l = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
d = {'a': 1, 'b': 2, 'c': 3}
t = (1,2,3,4,5)
s = 'abacdefg'

#list
for i in l:
	print(i)

#dic
for i in d:
	print(i)
for i in d.values():
	print(i)
for k,v in d.items():
	print('%s : %s' % (k,v))

#tuple
for i in t:
	print(i)

#string
for i in s:
	print(i)

from collections import Iterable
print(isinstance(l, Iterable))
print(isinstance(d, Iterable))
print(isinstance(t, Iterable))
print(isinstance(s, Iterable))

#index and value
for i,value in enumerate(['A','B','C']):
	print(i,value)

#mutil symbol
for x,y in [(1,1),(2,4),(3,9)]:
	print(x,y)


