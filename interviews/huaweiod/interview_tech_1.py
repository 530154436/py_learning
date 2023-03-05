#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/26
@function:
"""
def merge(intervals:list):
    if not intervals or len(intervals)==0:
        return [[]]

    sorted_intervals = sorted(intervals, key=lambda x:x[0])
    n = len(sorted_intervals)

    new_intervals = [sorted_intervals[0]]
    for i in range(1, n):
        if sorted_intervals[i][0]<=new_intervals[-1][1]:
            new_intervals[-1][1] = sorted_intervals[i][1]
        else:
            new_intervals.append(sorted_intervals[i])
    return new_intervals

l1 = [[1,3], [8,10], [2,6], [15,18]]
l2 = [[1,4], [4,5]]
print(merge(l1))
print(merge(l2))