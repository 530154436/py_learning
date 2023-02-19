#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Animal(object):
	def run(self):
		print('Animal is runing ...')

class Dog(Animal):
	def run(self):
		print('Dog is running ...')

	def eat(self):
		print('Eating meat ...')

class Timer(object):
	def run(self):
		print('Time is running ...')

def run_twice(animal):
	animal.run()
	animal.run()

animal = Animal()
dog = Dog()

animal.run()
dog.run()

print(isinstance(animal, Animal))
print(isinstance(dog, Animal))
print(isinstance(animal, Dog))
print(isinstance(dog, Dog))

run_twice(animal)
run_twice(dog)
run_twice(Timer())



