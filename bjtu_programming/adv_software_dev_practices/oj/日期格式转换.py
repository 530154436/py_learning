#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
请将格式如yyyy-m-d形式的日期转换为mm/dd/yyyy格式表示的日期。

输入
若干行，每行为一个yyyy-m-d形式的日期。

输出
对每行输入的日期，将其转换为mm/dd/yyyy格式表示的日期。

示例输入
2019-02-25
2019-02-25

2108-01-21
0962-09-02
6972-02-29
1111-1-1

示例输出
02/25/2019
"""

import sys

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    line = line.split('-')
    if len(line[1]) == 1:
        line[1] = '0' + line[1]
    if len(line[2]) == 1:
        line[2] = '0' + line[2]
    print(line[1] +'/'+line[2]+'/'+line[0])


