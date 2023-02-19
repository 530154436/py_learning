#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
若干32位整数求和。

输入
输入数据的第一行为一个整数TT，表示有TT组测试数据，每组为一行。随后的TT行中，每行第第一个数为一个整数NN，随后有NN个整数。

输出
对每组输入，在单独的行中输出结果，每两组结果之间以单个空行分隔。

示例输入
3
4 1 2 3 4
5 1 2 3 4 5
3 1 2 3
示例输出
10

15

6
"""

import sys

i =0

while True:
    sum = 0
    line = sys.stdin.readline().strip()
    if not line:
        break
    if (i != 0):
        list = line.split(' ')
        for j in list[1:]:
            sum = sum + int(j)
        if(i==1):
            print(sum)
        else:
            print('\n'+str(sum))
    i=i+1


