#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
请通过函数实现，输出底边长为 nn 的镂空等腰三角形。

输入
标准输入，包括两部分：c,n(0 \lt n \le 100,)c,n(0<n≤100,)，cc为指定输出的ASCII字符，nn为指定的边长。

输出
用指定的字符输出边长为nn的镂空等腰三角形。

示例输入
x 3
示例输出
    x
   x x
  x   x
 xxxxxxx
x x x x x
(n-1)个空格+x+空格x
"""

import sys

line = sys.stdin.readline().strip()
list = line.split(' ')
x = list[0]
len = int(list[1])
if(len==0):
    print(x)
else:
    sp = ' '*(len-1)+x
    print(sp)
    for i in range(1,len-1):
        sp = ' '*(len-i-1) + x + ' '*(2*i-1) + x
        print(sp)
    sp = (x+' ')*(len-1) + x
    print(sp)