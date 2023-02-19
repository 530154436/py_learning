#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
给定一个整数数组，请求出该数组中两数之差（绝对值）的最小值。
https://leetcode-cn.com/problems/smallest-difference-lcci/

要求单独定义函数实现。

输入
第一行为一个正整数n(1 \lt n \le 10000)n(1<n≤10000)，随后第二行为n个整数。

输出
该数组中两数之差（绝对值）的最小值。

示例输入
5
105 7 9 16 -31
示例输出
2
"""
import sys
line1 = sys.stdin.readline().strip()
n = int(line1)

line2 = sys.stdin.readline().strip()
nums = sorted(map(int, line2.split(' ')))

i, min_abs = 1, sys.maxsize
while i<n:
    a, b = nums[i-1], nums[i]
    _abs = b - a
    if _abs < min_abs:
        min_abs = _abs
    i += 1

print(min_abs)
