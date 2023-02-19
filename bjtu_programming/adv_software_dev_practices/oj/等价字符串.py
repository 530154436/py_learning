#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
有两个长度相同的字符串，均由字母A-Z构成，长度不超过100。
请判断是否可以把其中一个字符串的各个字母重排
然后对26个字母做一个一一映射，使得两个字符串相同。

如JWPUDJSTVP重排后可以得到WJDUPSJPVT，
然后把每个字母映射到它前一个字母(B->A, C->B, ..., Z->Y, A->Z)，
得到VICTORIOUS。

输入
两个字符串。

输出
若可以请输出YES，否则输出NO。

示例输入
ABBCFEA
CCGGHJB
示例输出
YES
思路：首先把映射前的字符串算出来，再对比原字符串是否字母组成一致
"""
import sys
from collections import Counter
str1 = sys.stdin.readline().strip()
str2 = sys.stdin.readline().strip()

count1 = {}
count2 = {}
for i in str1:
    count1[i] = str1.count(i)
value1 = Counter(count1.values())

for j in str2:
    count2[j] =str2.count(j)
value2 = Counter(count2.values())

if value1==value2:
    print('Yes')
else:
    print('No')

