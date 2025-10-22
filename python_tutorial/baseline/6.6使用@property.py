#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Student01(object):

	def get_score(self):
		return self._score

	#限制score的范围
	def set_score(self, score):
		if not isinstance(score, int):
			raise ValueError('score must be integer')
		if 0 <= score <= 100:
			self._score = score
		else:
			raise ValueError('score must between 0 - 100 !')

def test01():
	s = Student01()
	s.set_score(60)
	print(s.get_score())

	#ValueError: score must between 0 ~ 100!
	# s.set_score(-10)
	
	#ValueError: score must be integer
	# s.set_score('12')

class Student02(object):

	@property
	def score(self):
		return self._score

	#限制score的范围
	@score.setter
	def score(self, score):
		if not isinstance(score, int):
			raise ValueError('score must be integer')
		if 0 <= score <= 100:
			self._score = score
		else:
			raise ValueError('score must between 0 - 100 !')

def test02():
	s = Student02()
	s.score = 60
	print(s.score)

	#ValueError: score must between 0 - 100 !
	# s.score = -10
	# print(s.score)

class Student03(object):

	@property
	def birth(self):
		return self._birth

	@birth.setter
	def birth(self, birth):
		self._birth = birth

	#age是一个只读属性
	@property
	def age(self):
		return 2017 - self._birth

def test03():
	s = Student03()
	s.birth = 1997
	print(s.birth)
	print(s.age)

#练习
class Screen(object):
	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, width):
		self._width = width
	
	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, height):
		self._height = height

	@property
	def resolution(self):
		return self._width * self._height

def test():
	s = Screen()
	s.width = 1024
	s.height = 768
	print(s.resolution)
	assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution

if __name__ == '__main__':
	# test01()
	# test02()
	test03()
	test()




