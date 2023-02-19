#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
有两个长度相同的字符串，均由字母A-Z构成，长度不超过100。
请判断是否可以把其中一个字符串的各个字母重排，然后对26个字母做一个一一映射，使得两个字符串相同。

如JWPUDJSTVP重排后可以得到WJDUPSJPVT，
然后把每个字母映射到它前一个字母(B->A, C->B, ..., Z->Y, A->Z)，得到VICTORIOUS。

输入
两行字符串。

输出
若可以请输出两行，第一行为YES，第二行为对应的一个映射。否则输出NO。

示例输入
ABBCFEA
CCGGHJB
示例输出
YES
A->C B->G C->H F->J E->B
"""
import sys
from collections import Counter
str1 = sys.stdin.readline().strip()
str2 = sys.stdin.readline().strip()

count1 = {}
count2 = {}
for i in str1:
    count1[i] = str1.count(i)

for j in str2:
    count2[j] =str2.count(j)

if Counter(count1.values())==Counter(count2.values()):
    print('YES')
    out = ''
    for key1,key2 in zip(count1.keys(),count2.keys()):
        out = out + key1 + '->' + key2 + ' '
    print(out.strip())
else:
    print('NO')