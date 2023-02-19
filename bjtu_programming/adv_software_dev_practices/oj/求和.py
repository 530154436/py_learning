#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
计算若干十六进制数的和。

输入
输入有若干行，每行为由空格分隔的若干数十六进制整数（不超过10000个），如：

5 A
输出
控制台输出，对每行输入，输出该行十六进制数的和，用十进制表示。如：

15
示例输入
A B
0xB 0xC
示例输出
23

"""
import sys
while True:
    num = 0
    line = sys.stdin.readline().strip()
    if not line:
        break
    list = line.split(' ')
    for x in list:
        num = num + int(x,16)
    print(num)


