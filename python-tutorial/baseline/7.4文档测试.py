#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import doctest

m = re.search('(?<=abc)def', 'abcdef')
print(m.group())

def abs(n):
	'''
	Function to get absolute value of number.

    Example:

    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0

	'''
	return n if n >= 0  else (-n)

# IndentationError: unindent does not match any outer indentation level
# 原因：混用TAB和空格
def fact(n):
    '''

    Simple test

    >>> fact(1)
    1

    >>> fact(0)
    Traceback (most recent call last):
        ...
    ValueError

    >>> fact(5)
    120

    '''
    if n < 1 :
    	raise ValueError()
    if n == 1 :
        return 1
    return n * fact(n - 1)

if __name__ == '__main__':
	doctest.testmod()



