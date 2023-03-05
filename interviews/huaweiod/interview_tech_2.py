#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/26
@function:
"""
def two_sum_1(nums, target):
    sorted_nums = sorted(nums)
    i, j = 0,len(nums)-1
    while i<j:
        if sorted_nums[i]+sorted_nums[j]==target:
            return i,j
        elif sorted_nums[i]+sorted_nums[j]<target:
            i += 1
        else:
            j -= 1
    return -1,-1

nums = [2,7,11,15]
print(two_sum_1(nums, 9))