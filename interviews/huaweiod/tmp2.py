#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/17
@function:
"""
import sys

def L(s):
    return s[4:6] + s[2:4] + s[0:2][::-1]

def R(s):
    return s[4:6][::-1] + s[2:4] + s[0:2]

def F(s):
    return s[0:2] + s[4:6] + s[2:4][::-1]

def B(s):
    return s[0:2] + s[4:6][::-1] + s[2:4]

def A(s):
    return s[2:4][::-1] + s[0:2] + s[4:6]

def C(s):
    return s[2:4] + s[0:2][::-1] + s[4:6]

action_func = {
    'A':A,
    'B':B,
    'C':C,
    'L':L,
    'R':R,
    'F':F
}

def process(line):
    s = '123456'
    for action in line:
        func = action_func.get(action)
        s = func(s)
    return s

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