#!/usr/bin/env python3
# -*- coding: utf-8 -*-

g = (x*x for x in range(1,11))
print(g)
print(next(g))
print(next(g))
print(next(g))
print(next(g))

for n in g:
	print(n)

while True:
	try:
		x = next(g)
		print('g:',x)
	except StopIteration as e:
		print('Generator return value:',e.value)
		break


#斐波拉契数列
def fib(max):
	n,a,b =0,0,1
	while n<max :
		print(b)
		a,b = b,a+b
		n += 1
	return 'done'

print(fib(6))

# generator
def fib(max):
	n,a,b =0,0,1
	while n<max :
		yield b
		a,b = b,a+b
		n += 1
	return 'done'

print(fib(6))

def odd():
	print('step 1')
	yield 1
	print('step 2')
	yield 2
	print('step 3')
	yield 3

for x in odd():
	print(x)

#杨辉三角
def triangles():
	l = [1]
	while True:
		yield l
		l = [1] + [l[x] + l[x+1] for x in range(len(l)-1)] +[1]
		
		
n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break




