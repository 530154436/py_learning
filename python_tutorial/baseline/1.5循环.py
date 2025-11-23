#!/usr/bin/env python3
# -*- coding: utf-8 -*-
names = ['edward','zhengchubin']
for term in names:
	print(term)

numbers = [1,2,3,4,5,6,7,8,9,10]
numbers = range(101)
print(numbers)
sum = 0
for num in numbers:
	sum += num
print(sum)

n = 100
sum = 0
while n > 0:
	sum += n
	n -= 1
print(sum)

# 作业
names = ['edward','zhengchubin']
for name in names:
	print('Hello, %s!' % name)