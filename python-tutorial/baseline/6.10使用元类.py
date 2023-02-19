#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)

h = Hello()

# <class 'type'>
print(type(Hello))

# <class '__main__.Hello'>
print(type(h))


def fn(self, name='world'):
	print('Hello, %s' % name)

Hello = type('Hello', (object, ), dict(hello = fn))
h = Hello()

# Hello, world
h.hello()

# <class 'type'>
print(type(Hello))

# <class '__main__.Hello'>
print(type(h))

##元类  http://blog.jobbole.com/21351/






