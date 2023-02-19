#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2022/06/05
@function:
"""
import random
random.seed(1)

_min, _max = 1, 20

for i in range(2):
    i = f'{i+1}'
    i = '0' * (3 - len(i)) + i
    file = f'data/test-in1/{i}.txt'

    writer = open(file, mode='w', encoding='utf8')
    for j in range(10000):
        string = f'{str(random.randint(_min, _max))},' \
                 f'{str(random.randint(_min, _max))},' \
                 f'{str(random.randint(_min, _max))}'
        writer.write(string)
        writer.write('\n')
        writer.flush()
    writer.close()
