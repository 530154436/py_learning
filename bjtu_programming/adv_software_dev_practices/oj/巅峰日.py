#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
大贤者福尔经过长期的研究后发现，人的体力、智商和情商和运气具有周期性，会有高峰和低估，并且呈现出周期性变化的规律。
在每一个周期中会有一天是高峰，这一天人会在某个方便表现的非常出色。尽管如此，由于这些周期的长度不一致，
通常情况下几个周期的高峰不会在同一天出现。但大众又都希望哪一天是自己的巅峰日，在这一天中，自己的体力、智商和情商和运气都达到高峰。

输入
输入数据有若干组，每一组包括两行数据，第一行包括4个正整数，分别为体力、智商和情商和运气的周期，
已知最大周期不超过50。第二行包括5个非负整数p,i,e,l,d，分别表示体力、智商、情商、和运气在一年中第一次达到高峰的时间
（从一年的第一天开始算起，第一天记为0），d为计算的开始时间（从一年第一天开始的天数）。所有时间非负且小于365。

输出
对每组测试数据，在单独的行中输出结果。先输出当前测试样例的组号Case x:，
x为测试样例编号，随后输出第一个巅峰日距离给定日期 d的天数。
若在有生之年都无法找到这样的日子，则输出No such days.。所谓有生之年是指不超过上述周期之积后一年的日期范围。

示例输入
23 28 33 1
0 0 0 0 0
23 28 33 1
0 0 0 0 100
23 28 33 1
5 20 34 0 325
23 28 33 1
4 5 6 0 7
23 28 33 1
283 102 23 0 320
23 28 33 1
203 301 203 0 40
39 3 48 21
31 323 144 294 146
示例输出
Case 1: 21252
Case 2: 21152
Case 3: 19575
Case 4: 16994
Case 5: 8910
Case 6: 10789
Case 7: No such days.

理解：
1、周期<365
2、每年中第一次到达巅峰的日期
（1）<365
（2）可能比周期还大
比周期小的时候怎么算？
比周期大的时候怎么算？

需要计算每个巅峰日在周期里面是第几天

算法：
字典：
{体力：[周期、第一天]，智商：[周期、第一天]，情商：{周期、第一天}，运气：{周期、第一天}}
1、a,b,c,d
x / a =a1
x / b =b1
x / c =c1
x / d =d1
"""
import sys

jishi = 1

while True:
    data = {}

    line1 = sys.stdin.readline().strip()
    if not line1:
        break
    line1 = line1.split(' ')
    line2 = sys.stdin.readline().strip()
    line2 = line2.split(' ')

    # 距离给出的时间d
    d = int(line2[4]) + 1
    # 巅峰日记录
    b = 1
    for i in range(0,4):
        data[int(line1[i])] = [int(line2[i])+1,(int(line2[i])+1)%int(line1[i])]
        b = b * int(line1[i])

    # 找到巅峰日第一天最大的数值
    maxd = []
    for i in data.values():
        maxd.append(i[0])
    maxdd = max(maxd)

    # 周期排序
    kk = list(data.keys())
    kk.sort(reverse=True)

    # 与最大周期相除，如果余数等于第几天，则继续，否则直接加最大的周期，继续与倒数第二的除余
    while True:
        if maxdd<= d:
            maxdd = d+1
        if maxdd % kk[0] == data[kk[0]][1]:
            if maxdd%kk[1] == data[kk[1]][1]:
                if maxdd%kk[2] == data[kk[2]][1]:
                    if maxdd%kk[3] == data[kk[3]][1]:
                        if (maxdd - d)>=0:
                            print('Case' + ' ' + str(jishi) + ': ' + str(maxdd - d))
                            break
            maxdd = (int(maxdd//kk[0])+1)*kk[0] + data[kk[0]][1]
        elif maxdd % kk[0] > data[kk[0]][1]:
            maxdd = (int(maxdd//kk[0])+1)*kk[0] + data[kk[0]][1]
        else:
            maxdd = (int(maxdd // kk[0]) ) * kk[0] + data[kk[0]][1]
        if (maxdd-1) > b:
            print('Case' + ' ' + str(jishi) + ': ' + 'No such days')
            break

    jishi = jishi + 1

