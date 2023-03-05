#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/17
@function:
"""
import sys

def process(line):
    nums = line.split(' ')
    c = int(nums[0])
    b = int(nums[1])

    sums = []
    for num in nums[2:]:
        h_num_str = hex(int(num)).replace('0x', '')
        h_num_str = '0'*(8-len(h_num_str))+h_num_str

        hex_nums_str = [h_num_str[end - 2:end]for end in [2,4,6,8]]
        ten_nums = [int(i, 16) for i in hex_nums_str]
        # print(num)
        # print(h_num_str)
        # print(hex_nums_str)
        # print(ten_nums)
        # print(sum(ten_nums))
        # print()
        sums.append(sum(ten_nums))
    mods = [s%b for s in sums]
    d = {}
    for m in mods:
        if m>=c:
            continue
        if m not in d:
            d[m] = 0
        d[m] += 1
    # print(d)
    if len(d)>0:
        s_d = sorted(d.items(), key=lambda x:x[1], reverse=True)
        # print(s_d)
        return s_d[0][1]
    else:
        return 0

try:
    lines = []
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        lines.append(line)

    for line in lines:
        print(process(line))
except Exception as e:
    pass