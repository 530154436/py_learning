#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
给定一个整数数组，请求出该数组中两数之差（绝对值）的最小值，并确定对应元素的位置。

输入
第一行为一个正整数n(1 \lt n \le 10000)n(1<n≤10000)，随后第二行为n个整数。

输出
该数组中两数之差（绝对值）的最小值及对应元素在输入数组中的位置索引，索引从1开始计数，以空格分隔。若有多组，输出任意一组即可。

示例输入
5
105 7 9 16 -31
示例输出
2 2 3
"""
import sys
line1 = sys.stdin.readline().strip()
n = int(line1)

line2 = sys.stdin.readline().strip()

def find_min(n, line2):
    idx_mapper = {}
    for i, num in enumerate(map(int, line2.split(' ')), start=1):
        if num in idx_mapper:
            print(0, idx_mapper.get(num), i)
            return
        idx_mapper[num] = i

    nums = sorted(idx_mapper.keys())

    i, min_a, min_b, min_abs = 1, nums[0], nums[1], sys.maxsize
    while i < n:
        a, b = nums[i - 1], nums[i]
        _abs = b - a
        if _abs < min_abs:
            min_abs = _abs
            min_a = a
            min_b = b
        i += 1

    i, j = idx_mapper.get(min_a), idx_mapper.get(min_b)
    if i > j:
        print(min_abs, j, i)
    else:
        print(min_abs, i, j)

find_min(n, line2)