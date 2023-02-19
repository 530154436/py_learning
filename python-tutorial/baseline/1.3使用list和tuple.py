#!/usr/bin/env python3
# -*- coding: utf-8 -*-
classMates = ['edward','bob',12]

print(len(classMates))
print(classMates[0])
print(classMates[-1])

classMates.append('mary')
print(classMates)

classMates.insert(1,'baby')
print(classMates.pop(1))


classMates = ('edward','zhengchubin',11)
print(classMates)

classMates = ('a','b',['A','B'])
print(classMates)
print(classMates[2][1])

t=(1,)

t='a'
print(('a', 'b', ['X', 'Y']))

L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
S = (L[0][0],L[1][1],L[2][2])
print('#打印Apple:\n%s\n#打印Pythonle:\n%s\n#打印Pythonle:\n%s\n' % S)