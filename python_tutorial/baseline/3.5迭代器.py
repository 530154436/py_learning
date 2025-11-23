#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Iterable
from collections import Iterator

print(isinstance([], Iterable))
print(isinstance((), Iterable))
print(isinstance({}, Iterable))
print(isinstance(None, Iterable))
print(isinstance('1232f', Iterable))

print(isinstance((x for x in range(10)), Iterator))
print(isinstance([], Iterator))
print(isinstance((), Iterator))
print(isinstance({}, Iterator))
print(isinstance(None, Iterator))
print(isinstance('1232f', Iterator))

print(isinstance(iter([]), Iterator))
print(isinstance(iter(()), Iterator))

for x in [1,2,3,4,5]:
	pass

# 首先获得Iterator对象
it = iter([1,2,3,4,5])
# 循环:
while True:
	try:
		# 获得下一个值:
		x = next(it)
	except StopIteration:
		# 遇到StopIteration就退出循环
		break;




