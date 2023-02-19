#!/usr/bin/env python3
# -*- coding: utf-8 -*-
s = input('请输入年龄：')
age = int(s)
if age >= 18:
	print('your age is %d' % age)
	print('adult')
else:
	print('your age is %d' % age)
	print('teenager')


s1=input('请输入身高(m):')
s2=input('请输入体重(kg):')
height=float(s1)
weight=float(s2)
BMI=weight/(height**2)
if BMI<18.5:
	print('过轻')
elif BMI<=25:
	print('正常')
elif BMI<=28:
	print('过重')
elif BMI<=32:
	print('肥胖')
else:
	print('严重肥胖')