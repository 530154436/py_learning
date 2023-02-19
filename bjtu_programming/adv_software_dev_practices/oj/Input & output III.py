#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
计算两个32位整数A和B的和！

输入
输入数据有多组，每组为一行，包括两个32位整数。若两个整数均为0，表示输入结束。

输出
对每组输入，在单独的行中输出结果。

示例输入
1 2
-1 1
0 0
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
    if ((a,b) == ('0','0')):
        break
    print(int(a) + int(b))