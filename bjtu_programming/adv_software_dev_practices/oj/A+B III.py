#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
计算两个整数A和B的和。
输入
输入有若干行，每行为由空格分隔的一对整数A和B，如： 5 12

输出
输出数据A和B的和。

示例输入
25 33
示例输出
58
提示
A和B可能很大，最大不超过1000位十进制数。
"""

import sys

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    line = line.split()
    out = int(line[0]) + int(line[1])
    print(str(out))