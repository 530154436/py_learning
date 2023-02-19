#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
一篇文章由有若干个单词构成，小A希望知道文章中有哪些特殊单词。
所谓特殊单词是指，构成这个单词的字母经过顺序变换形成的一个新单词也出现在文章中。
与原单词构成的字母对比，新单词的字母可以有大小变化。

小A希望知道文章中这样的特殊单词有哪些，您能帮他找出来吗？

输入
输入数据有若干行，每行为一个字符串，由空格分隔开，
单词由大小写字符及数字构成，每个单词长度不超过30个ASCII码字符。
若该行字符为#，表示输入结束。

输出
按字典序输出所有的特殊单词。所有特殊单词按其第一次在文章中出现的形式输出，每行输出一个单词。

示例输入
a aa sd 12 aaa Bd dB
BD c a 21 A
aa aaa
#
示例输出
12
Bd
a
"""

import sys
from copy import deepcopy
from collections import Counter

# 记录所有的单词
ls = []

# 记录特殊单词
out = []

while True:
    line = sys.stdin.readline().strip()
    if line == '#':
        break
    line = line.split(' ')
    for i in line:
        ls.append(i)

lis = list(set(ls))
lis.sort(key=ls.index)
new_lis = deepcopy(lis)

for i in lis:
    try:
        new_lis.remove(i)
        for j in new_lis:
            if Counter(i.upper()) == Counter(j.upper()):
                out.append(i)
                new_lis.remove(j)
    except Exception:
        pass

out = list(set(out))
out.sort()
print('\n'.join(out))

        














