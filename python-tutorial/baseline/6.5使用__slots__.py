#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from types import MethodType

class Student01(object):
	pass

def set_age(self, age):
	self.age = age

def set_score(self, score):
	self.score = score

def test01():
	s = Student01()
	s.name = 'Edward'
	print(s.name)

	s.set_age = MethodType(set_age, s)
	s.set_age(12)
	print(s.age)

	#AttributeError: 'Student01' object has no attribute 'set_age'
	# s1 = Student01()
	# s1.set_age(99)
	# print(s1.age)

	Student01.set_score = set_score
	s.set_score(100)
	print(s.score)

	s2 = Student01()
	s2.set_score(99)
	print(s2.score)

class Student02(object):
	__slots__ = ('name', 'age')

class GraduateStudent(Student02):
	pass

def test02():
	s = Student02()
	s.name = 'Edward'
	print(s.name)

	#AttributeError: 'Student' object has no attribute 'score'
	# s.score = 12
	# print(s.score)

	g = GraduateStudent()
	g.score = 199
	print(g.score)

if __name__ == '__main__':
	test01()
	test02()



