#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

def test_try_except():
	try:
		print('trying ...')
		r = 10/int('1')
		print('result: ', r)
	except ZeroDivisionError as e:
		print('except: ', e)
	except ValueError as e:
		print('except: ', e)
	else:
		print('no error')
	finally:
		print('finally ...')
	print('END')


def foo01(s):
	return 10 / int(s)

def bar(s):
	return foo01(s) * 2

def main():
	try:
		bar('0')
	except BaseException as e:
		print('Error: ', e)
		logging.exception(e)

def test_base_exception():
	main()
	print('END')

class FooError(ValueError):
	pass

def foo02(s):
	n = int(s)
	if n == 0:
		raise ValueError('invalid value: %s' % s)
	return 10/n

def bar():
	try:
		foo02('0')
	except ValueError as e:
		print('ValueEroor!')
		raise

def test_raise():
	foo02('1')
	bar()

def test_error_trans():
	try:
		10/0
	except ZeroDivisionError as e:
		raise ValueError('input error !')

if __name__ == '__main__':
	test_try_except()
	test_base_exception()
	test_raise()
	test_error_trans()

