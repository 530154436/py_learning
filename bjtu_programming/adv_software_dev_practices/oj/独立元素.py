#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
给定一个整数数组，请按从大到小的顺序输出该数组中元素，相同的元素只输出一次。

输入
第一行为一个正整数N(1<N≤10000)，随后第二行为N个整数，整数间以空格分隔。

输出
按从大到小的顺序输出满足条件的元素。

示例输入
5
105 7 9 16 -31
示例输出
105 16 9 7 -31
"""

import sys

line1 = sys.stdin.readline().strip()
line2 = sys.stdin.readline().strip().split(' ')
line2 = list(set(map(int,(line2))))
line2.sort(reverse=True)
print(line2)
out = ''
for i in line2:
    out = out + str(i) + ' '
print(out.strip())
