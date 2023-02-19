#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
命令行中有一个列目录的程序，可以按照指定的方式将目录中的文件罗列出来。
小A想进一步改进列表程序，希望在给定的显示宽度限制下用最少的行格式化输出所有的文件名，且排在前面的行尽可能满列。

显示规则为：文件列表按字典序左对齐的方式显示为若干列，列宽由文件名的最大长度确定，列间用2个空格分割，最后一列后无空格。

输入
输入数据有若干组，每组为待罗列的文件名列表，格式如下：
每组的第一行为空格分隔的两个整数n,w(0<n≤w)，
分别为该组文件的数量和一行能够显示的宽度。随后的n行中，
每行为一个文件名，保证每个文件名最长不超过指定的显示宽度。

输出
对每组输入，先根据要求的宽度输出对应个-，
随后按要求输出若干列格式化的文件名列表，
所有列表中文件名自上而下、从左到右按字典序排列。

示例输入
20 60
a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
10 10
a
b
c
d
e
f
g
h
i
j

示例输出
------------------------------------------------------------
a  b  c  d  e  f  g  h  i  j  k  l  m  n  o  p  q  r  s  t
----------
a  d  g  i
b  e  h  j
c  f
"""

import sys

while True:
    num = sys.stdin.readline().strip()
    if not num:
        break
    num = num.split(' ')
    print('-'*int(num[1]))


    # 各组数据输出的各行用str记录
    out = ''
    n = 0

    for i in range(0,int(num[0])):
        name = sys.stdin.readline().strip()
        if (n+len(name)) <= int(num[1]):
            out = out + name + '  '
            n = len(out)
        else:
            print(out.strip())
            out = name + '  '
            n = 0
    print(out.strip())
