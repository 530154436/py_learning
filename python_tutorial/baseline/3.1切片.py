#!/usr/bin/env python3
# -*- coding: utf-8 -*-

L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']

print(L[0:3])
print(L[-1])

L = list(range(100))
print(L[-10:])
print(L[:10])
print(L[::5])
print(L[-2:-10:-2])  # 从倒数第二到倒数第十间隔为2反向取值
print(L[-1::-1])  # L反向取全部值
print(L[30:20:-1])  # 从L[29]到L[19]反向取值


tuple = (1,2,3,4,5)
print(tuple[:3])

print('adfdf'[:3])

L = list(range(10))
print(L[::2])
L[::2] = [-i for i in L[::2]]
print(L[::2])