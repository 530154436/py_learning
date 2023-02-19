#!/usr/bin/env python3
# -*- coding: utf-8 -*-

l1 = sorted([46, 5, 32, -12])
l2 = sorted([46, 5, 32, -12], key=abs)

print(l1)
print(l2)

s1 = sorted(['edward', 'bob', 'andy', 'Andy'])
s2 = sorted(['edward', 'bob', 'andy', 'Andy'], key=str.lower)
s3 = sorted(['edward', 'bob', 'andy', 'Andy'], key=str.lower, reverse=True)

print(s1)
print(s2)
print(s3)

# 练习
def by_name(t):
	return t[0]

def by_score(t):
	return t[1]

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
L2 = sorted(L, key=by_name)
L3 = sorted(L, key=by_score)[::-1]

print(L2)
print(L3)






