#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
有N张卡牌，每张卡牌上标记有一个正整数。
为管理方便对卡牌按数值大小进行了从小到大的排序，
现希望知道是否存在标记有某个数值的卡牌，以及其排序后的位置。
排序后第一张卡牌的位置记为1，以此类推，第N章卡牌的位置记为N。

输入
输入有多组数据，每组数据包含三行整数，
第一行为空格分隔的两个正整数N,Q，分别表示卡牌张数和问题数，
第二行为卡牌上的数值，第三行为Q空格分隔查询的数值。

输出
对每组数据，第一行输出Case #T:，其中T为当前数据组的编号，从1开始；
随后对每个查询单独输出一行。
若存在该编号，输出q found at x，q为查询编号的数值，x为其排序后的位置；
若不存在，输出q not found，q为查询的数值。

示例输入
4 1
2 3 5 1
5
5 2
1 3 3 3 1
2 3
示例输出
Case #1:
5 found at 4
Case #2:
2 not found
3 found at 3

5 2
6 3 9 5 10
3 0
"""


import sys

n = 1
while True:
    line1 = sys.stdin.readline().strip()
    if  not line1:
        break

    line2 = sys.stdin.readline().strip()
    list2 = list(map(int, line2.split(' ')))
    list2.sort()

    line3 = sys.stdin.readline().strip()
    line3 = list(map(int,line3.split(' ')))

    print('Case #'+ str(n) + ':')
    for i in line3:
        if i in list2:
            print( str(i) + ' found at ' + str(list2.index(i)+1))
        else:
            print(str(i) + ' not found')
    n = n + 1
