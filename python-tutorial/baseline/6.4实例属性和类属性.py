#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Student(object):
	name = 'Student'
	def __init__(self, name):
		self.name = name

s = Student('Bob')
s.score = 90

print(s.name)
print(Student.name)

del s.name
print(s.name)



