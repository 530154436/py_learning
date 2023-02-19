#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def is_odd(n):
	return n%2==1

l1 = list(filter(is_odd, [1,2,3,4,5,6,7,8,9]))
print(l1)

def no_empty(s):
	return s and s.strip()

l2 = list(filter(no_empty, ['A', '', 'C', None, '   ']))

print(l2)

def _not_divisible(n):
	return lambda x: x % n > 0

def _odd_iter():
	n = 1
	while True:
		n = n + 2
		yield n

def primes():
	yield 2
	it = _odd_iter()
	while True:
		n = next(it)
		yield n
		it = filter(_not_divisible(n), it)

l3 = []
for n in primes():
    if n < 100:
        l3.append(n)
    else:
        break
print(l3)

#练习1 回数是指从左向右读和从右向左读都是一样的数，例如12321，909。请利用filter()滤掉非回数：
def is_palindrome(n):
	return str(n) == str(n)[::-1]

output = filter(is_palindrome, range(1, 100))
print(list(output))





