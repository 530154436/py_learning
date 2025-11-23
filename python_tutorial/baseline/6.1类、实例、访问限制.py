#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student(object):
	def __init__(self, name, score):
		self.__name = name
		self.__score = score

	def get_name(self):
		return self.__name

	def get_score(self):
		return self.__score

	def set_name(self, name):
		self.__name = name

	def set_score(self, score):
		if 0 <= score <= 100:
			self.__score = score
		else:
			raise ValueError('bad score')

	def print_score(self):
		print('%s : %s' % (self.__name, self.__score))

	def get_grade(self):
		if self.__score >= 90:
			return 'A'
		elif self.__score >= 80:
			return 'B'
		elif self.__score >= 60:
			return 'C'
		else:
			return 'D'

def test_student():
	edward = Student('zhengchubin',100)
	print(Student.__name__)
	print(edward.get_name())
	print(edward._Student__name)

	edward.set_name('edward')
	edward.set_score(10)

	edward.print_score()
	print(edward.get_grade())


if __name__ == '__main__':
	test_student()




