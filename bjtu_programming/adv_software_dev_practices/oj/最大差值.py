#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
给定一个整数数组，请求出该数组中两数之差（绝对值）的最大值。 要求单独定义函数实现。

输入
第一行为一个正整数n(1<n≤10000)，随后第二行为n个整数。

输出
该数组中两数之差（绝对值）的最大值。

示例输入
5
105 7 9 16 -31
示例输出
136
"""
big = 0
import sys
line1 = sys.stdin.readline().strip()
n = int(line1)

line2 = sys.stdin.readline().strip()
nums = list(map(int, line2.split(' ')))

_min, _max = nums[0], nums[0]
for num in nums:
    if _min > num:
        _min = num
    if _max < num:
        _max = num
print(_max - _min)
