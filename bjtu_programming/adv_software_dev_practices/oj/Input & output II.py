#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
计算两个32位整数A和B的和！

输入
输入数据的第一行为一个整数TT，表示有TT组数据。随后的TT行中，每行有两个整数A和B。

输出
对每组输入，在单独的行中输出结果。

示例输入
2
1 2
-1 1
示例输出
3
0

"""

import sys

i=0
while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    if(i !=0):
        a, b = line.split(' ')
        print(int(a)+int(b))
    i = i+1