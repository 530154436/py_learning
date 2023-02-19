#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pdb
logging.basicConfig(level = logging.INFO)

def foo(s):
	n = int(s)
	assert n != 0, 'n is zero'
	return 10/n

def test_assert():
	foo('0')

def test_logging():
	s = '0'
	n = int(s)
	logging.info('n = %d' % n)
	print(10 / n)

#python3 -m pdb 7.2调试.py
def test_pdb():
	s = '0'
	n = int(s)
	print(10/n)

if __name__ == '__main__':
	#test_assert()
	#test_logging()
	test_pdb()









