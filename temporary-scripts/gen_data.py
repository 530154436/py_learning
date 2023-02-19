#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2022/06/05
@function:
"""
import random
random.seed(2)

_min, _max = 1, 10000

for i in range(20):
    i = f'{i+1}'
    i = '0' * (3 - len(i)) + i
    file = f'data/test-in/{i}.txt'

    writer = open(file, mode='w', encoding='utf8')
    for j in range(1000):
        integer = random.randint(_min, _max)

        writer.write(str(integer))
        writer.write('\n')
        writer.flush()
    writer.close()

