#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def f(x):
	return x*x

def build(x,y):
	return lambda: x * x + y * y

l1 = list(map(lambda x:x*x, [1,2,3,4,5,6,7]))

print(l1)

b = build(2,2)

print(b())






