#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student01(object):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return 'Student object (name: %s)' % self.name

	__repr__ = __name__

def test_str():
	s = Student01('Edward')
	print(s)

# 斐波那契数列
class Fib(object):
	def __init__(self):
		self.a, self.b = 0, 1

	def __iter__(self):
		return self

	def __next__(self):
		self.a, self.b = self.b, self.a + self.b
		if self.a > 100:
			raise StopIteration()
		return self.a

	#按照下标取出元素
	def __getitem__(self, n):
		if isinstance(n, int):
			a, b = 1, 1
			for x in range(n):
				a, b = b, a+b
			return a
		if isinstance(n, slice):
			start = n.start
			stop = n.stop
			if start is None:
				start = 0
			a, b = 1, 1
			L = []
			for x in range(stop):
				if x >= start:
					L.append(a)
				a, b = b, a+b
			return L


def test_iter_next_getitem():
	for n in Fib():
		print(n)

	print(list(Fib()))

	f = Fib()
	print(f[0])
	print(f[5])

	print(f[3:7])

#__getattr__()方法
class Student02(object):

	def __init__(self):
		self.name = 'edward'

	def __getattr__(self, attr):
		if attr == 'score':
			# return 99
			return lambda : 25
		raise AttributeError('Student has not attribute %s ' % attr)

def test_getattr():
	s = Student02()
	print(s.score)
	print(s.score())

# REST API 动态绑定 URL
class Chain(object):

	def __init__(self, path = ''):
		self._path = path

	def __getattr__(self, path):
		return Chain('%s/%s' % (self._path, path))
	
	# 动态绑定用户名
	def users(self, user_name):
		return Chain('%s/%s' % (self._path, user_name))

	def __str__(self):
		return self._path

	__repr__ = __str__

def test_chain():
	print(Chain().status.user.timeline.list)
	print(Chain().users('Edward').repos)

# 定义__call__()方法，直接对实例进行调用
class Student03(object):

	def __init__(self, name):
		self.name = name

	def __call__(self):
		print('My name is %s' % 'chubin.zheng')

def test_call():
	s = Student03(object)
	s()
	print(callable(s))
	print(callable(str))
	print(callable(int))

if __name__ == '__main__':
	test_str()
	test_iter_next_getitem()
	test_getattr()
	test_chain()
	test_call()



