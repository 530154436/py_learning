#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

class Mydict(dict):

	def __init__(self, **kw):
		super().__init__(kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError as e:
			raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

def test_my_dict():
	d = Mydict(a=1, b=2)
	print(d['a'])

# 单元测试
class test_unit(unittest.TestCase):
	
	def test_init(self):
		d = Mydict(a=1, b='test')
		# __getattr__
		self.assertEqual(d.a, 1)
		# __getattr__
		self.assertEqual(d.b, 'test')
		self.assertTrue(isinstance(d, dict))

	# 继承自dict，测试dict的方法
	def test_key(self):
		d = Mydict()
		d['key'] = 'value'
		# __getattr__
		self.assertEqual(d.key, 'value')

	# 测试类属性的动态创建
	def test_attr(self):
		d = Mydict()
		# __setattr__()
		d.key = 'value'
		self.assertTrue('key' in d)
		self.assertEqual(d['key'], 'value')

	def test_keyerror(self):
		d = Mydict()
		with self.assertRaises(KeyError):
			value = d['empty']

	def test_attrerror(self):
		d = Mydict()
		with self.assertRaises(AttributeError):
			value = d.empty

	def setUp(self):
		print('setUp ...')

	def tearDown(self):
		print('tearDown ...')

if __name__ == '__main__':
	#test_my_dict()
	unittest.main()








