#!/usr/bin/env python3
# -*- coding: utf-8 -*-
dic = {'edward':24, 'paul':25, 'jason':35}
print(dic['edward'])

dic['edward'] = 30
print(dic['edward'])
print('edward' in dic)

print(dic.get('edward'))
dic.pop('edward')

print(dic.get('edward',5))

for word in dic:
	print(word)

s1=set([1,2,3])
print(s1)
s1.add(4)
print(s1)

s1.remove(4)
print(s1)

s2=set([1,2,4])
print(s1 & s2)
print(s1 | s2)










