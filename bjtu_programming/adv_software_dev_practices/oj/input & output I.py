#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
计算两个32位整数A和B的和！

输入
输入数据有多组，每组为一行，包括两个不超过二进制32位的整数。

输出
对每组输入，在单独的行中输出结果。

示例输入
1 2
-1 1

示例输出
3
0
"""
import sys

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    a, b = line.split(' ')
    print(int(a)+int(b))