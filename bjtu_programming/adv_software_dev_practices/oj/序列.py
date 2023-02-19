#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
有一个整数序列，序列中每个元素的质因数只有2,3,5，
该序列的前几个元素为1,2,3,4,5,6,8,9,10。
按惯例，1也作为序列中的元素，且是序列中的第一个元素。
现在感兴趣的是，给定一个位置nn(1≤n≤10000)，该序列中第n个元素是多少？

输入
输入有若干行，每行为一个整数n，为查询的元素位置。

输出
对每行输入，在单独的行中输出序列中对应位置的元素。

示例输入
1
2
3
7
8
9
10
11
示例输出
1
2
3
8
"""

import sys

# 存储需要输出元素的所有位置
sq = []
while True:
    k = sys.stdin.readline().strip()
    if not k:
        break
    sq.append(int(k))

# 输出元素位置的最大值，即对于所有的输入只找到maxn的元素就可以了
maxn = max(sq)
pr = [1]

# Q1记录乘以2的倍数；Q2记录乘以3的倍数；Q3记录5的倍数
Q = {}
Q[1] = {2}
Q[2] = {3}
Q[3] = {5}

if maxn == 1:
    print('1')
else:
    for i in range(2,maxn+1):
        min1 = min(Q[1])
        min2 = min(Q[2])
        min3 = min(Q[3])

        # 求最小值
        minn = min(min1,min2,min3)

        # 求最小值对应是哪个子队列
        indexd = {min1:1,min2:2,min3:3}
        j = indexd[minn]

        # 把最小值添加到队列中
        pr.append(minn)

        Q[j].remove(minn)

        if j==1:
            Q[1].add(2*minn)
            Q[1].add(3*minn)
            Q[1].add(5*minn)
        elif j==2:
            Q[2].add(3 * minn)
            Q[2].add(5 * minn)
        else:
            Q[3].add(5 * minn)

for i in sq:
    print(pr[i-1])
















