#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' a test module '
__author__ = 'Edward'

import sys

def _private_1(name):
	return 'Hello, %s' % name

def _private_2(name):
	return 'Hi, %s' % name

def greeting(name):
	if len(name) > 3:
		return _private_1(name)
	else:
		return _private_2(name)

def test():
	args = sys.argv
	if len(args) == 1 :
		print('Hello word!')
	elif len(args) == 2:
		print(greeting(args[1]))
		print('Hello, %s!' % args[1])
	else:
		print('Too many arguments!')

if __name__ == '__main__':
	test()




