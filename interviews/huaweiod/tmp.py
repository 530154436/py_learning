#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/17
@function:
"""
import sys

# 64:2,128:1,32:4,1:128
# 50,36,64,128,127
# true,true,true,false,false

def process(line1, line2):
    # 处理内存 粒度-数量
    if not line1 or not line2:
        return ''
    l_q = {}
    max_lidu = 0
    memories = line1.split(',')
    for memory in memories:
        lidu, quantity = memory.split(':')
        lidu, quantity = int(lidu), int(quantity)
        l_q[lidu] = quantity
        if max_lidu<lidu:
            max_lidu = lidu

    # 处理申请列表
    applies = [int(i) for i in line2.split(',')]

    # 申请内存
    allocated = [False]*len(applies)
    for i,apply in enumerate(applies):
        if apply>max_lidu:
            continue
        for free in range(apply, max_lidu+1):
            if l_q.get(free,0):
                allocated[i] = True
                l_q[free] -= 1
                break

    return ','.join([ 'true' if i else 'false' for i in allocated])

try:
    lines = []
    while True:
        line1 = sys.stdin.readline().strip()
        line2 = sys.stdin.readline().strip()
        if not line1:
            break
        lines.append((line1, line2))

    for line1, line2 in lines:
        print(process(line1, line2))
except Exception as e:
    raise e