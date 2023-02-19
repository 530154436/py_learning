#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./lib')
import util

print(util.power(3))

print(util.register('Judy','女'))

print(util.add_end01(['edward']))
print(util.add_end01())

print(util.calc01((1,2,4,5)))
print(util.calc01([1,2,4,5]))

print(util.calc02(1,2,4))
print(util.calc02(*(1,2,4,5)))
print(util.calc02(*[1,2,4,5]))

util.person01('edward',10, city='beijing', gender='man')
extra={'city':'beijing', 'gender':'man', 'job':'nlper'}
util.person01('edward',10, city=extra['city'],gender=extra['gender'])
util.person01('edward',10, **extra)
util.person02('edward',10, **extra)

util.person03('edward',10, city='beijing', gender='man')

util.f1(1,2,3,4,c='c',d='d')
util.f2(1,2,d='d',e='1',c='2')


