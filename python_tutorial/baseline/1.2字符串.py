#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print(ord('A'))

print('中')

print(chr(66))

print(chr(25991))

x=b'ABC'
print(x)

print('ABC'.encode('ascii'))
print('中文'.encode('utf-8'))

print(b'ABC'.decode('ascii'))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))

print(len('最后的天使'))
print(len(b'\xe4\xb8\xad\xe6\x96\x87'))

a='Hello , %s, you have %d yuan' % ('edward',1000)
print(a)

print('%d-%02d %%' % (3,1))

s1=72
s2=85
r=100*(s2-s1)/s1
print('成绩提升: %.1f %%' % r)



