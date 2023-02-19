#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
计算两个32位整数A和B的和！

输入
输入数据有多组，每组为一行，包括两个32位整数。

输出
对每组输入，在单独的行中输出结果，每两组结果之间以单个空行分隔。

示例输入
1 5
10 20
示例输出
6

30
"""
import sys

i=0
while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    a, b = line.split(' ')
    if(i==0):
        print(int(a)+int(b))
    else:
        print("\n"+str((int(a)+int(b))))
    i = i+1