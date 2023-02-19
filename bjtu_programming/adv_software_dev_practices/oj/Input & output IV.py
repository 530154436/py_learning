#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
若干32位整数求和。

输入
输入数据有多组，每组为一行，包括若干个32位整数。行首数字为该行中后续数字的个数，若行首的数值为0，表示输入结束。

输出
对每组输入，在单独的行中输出结果。

示例输入
5 1 2 3 4 5
2 -1 1
0
示例输出
15
0
"""

import sys

while True:
    sum=0
    line = sys.stdin.readline().strip()
    if not line:
        break
    list = line.split(' ')
    if (list[0] == '0'):
        break
    for i in list[1:]:
        sum = sum+int(i)
    print(sum)
