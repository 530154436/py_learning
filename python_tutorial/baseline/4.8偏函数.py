#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

print(int('12', base=10))
print(int('12', base=8))
print(int('11', base=2))

def int2(x, base=2):
	return int(x, base)

print(int2('101'))

int2 = functools.partial(int, base=2)

print(int2('111'))

kw={'base':2}
print(int('10010', **kw))
print(int2('100', **kw))

max2 = functools.partial(max, 10)
print(max2(5,6,7,8))



