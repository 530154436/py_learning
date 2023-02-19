#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
排队是日常生活中经常遇到的事情，如超市结账，餐厅就餐等。有时候，因为队伍实在是太长，或者比较着急，排队过程中经常会遇到插队的情况。

允许插队时，一个人到达餐厅时会先看看队列里面是否有熟人，如果发现了熟人，他就会插队并排到熟人的后面。如果没有熟人在排队，他就只能在队尾排队。有时候，队伍中的某个或某些相熟的同学实在不想排队了，他们就会离队。队伍中的人只有在轮到自己时，才会办理业务并离队。

小A正在研究允许插队的排队问题，他准备编写一个计算机程序，模拟排队的过程。他把相熟的人定义为若干小组，每个小组中的人都是相熟的，相熟的人排队时会插队。在此基础上，他定义了一系列指令，表示排队过程中发生的情况。

enqueue x: x开始排队；
dequeue： 队头的人办理完业务离队；
deqteam x：x及相熟的人（若存在）离队；
stop：停止模拟；
输入
输入数据有若干组，每组为的第一行为一个整数g，表示一共有多少个小组。
随后的g行中，每行表示一个小组。小组行的最前面为一个整数n，表示小组中有n个人，
随后有空格分隔的nn个名单，每个名字最长不超过10个字符，由大小写字母或数字构成。随后的若干行为排队模拟指令，
stop指令表示该组数据结束。

输出
对每组测试数据，在第一行输出一个Case #k:,k为测试数据的组号，从1开始。对于每个dequeue指令，若队列非空，则在单独的行中输出出队者的名字；对于每个deqteam指令，在单独的行中输出所有出队者的名字，以空格分隔。若队列为空，则不输出任何内容。

示例输入
2
3 101 102 103
3 201 202 203
enqueue 101
enqueue 201
enqueue 102
enqueue 202
deqteam 102
enqueue 203
dequeue
dequeue
dequeue
dequeue
dequeue
dequeue
stop
2
5 259001 259002 259003 259004 259005
6 260001 260002 260003 260004 260005 260006
enqueue 259001
enqueue 260001
enqueue 259002
enqueue 259003
enqueue 259004
enqueue 259005
dequeue
dequeue
enqueue 260002
enqueue 260003
deqteam 260002
dequeue
dequeue
dequeue
stop
0
示例输出
Case #1:
101 102
201
202
203
Case #2:
259001
259002
260001 260002 260003
259003
259004
259005

"""

import sys
pai = {}
case = 1

while True:
    yuan = {}
    yuans = {}

    line = sys.stdin.readline().strip()

    if not line:
        break

    if line == '0':
        break

    print('Case #' + str(case))
    case = case + 1

    zu = int(line)
    for i in range(1,zu+1):
        line = sys.stdin.readline().strip()
        # yuan  记录每组数据
        # yuans 记录每个数据对应的组别

        yuan[i] = line.split(' ')
        yuan[i] = yuan[i][1:]

        for j in yuan[i]:
            yuans[j] = i

    print(yuan)
    print(yuans)

    out = {}
    zhong = {}
    n = 1

    while True:
        # 排队的数据需要包含：1、排队的顺序；2、排队的人员所在的组
        # 排队的数据用dict存储，其中key代表顺序，value代表组员所在的组
        # 出队的时候从1开始遍历，找到对应的key
        # 用dict记录哪一组在队列里面，在哪个key里面
        line = sys.stdin.readline().strip()

        if line == 'stop':
            break

        try:
            line = line.split(' ')
            # line[0] 为命令，line[1]指数据
            # yuans[line[i]]代表元素所在的组

            szz = yuans[line[1]]  # 所在组

            if line[0] == 'enqueue':
                # 判断组在不在输出的dict里面，如果不在添加在输出的dict里，并且记录这一组在哪一行
                # 如果所在的组在输出的dict里面了，则找到这个组所在的行：out[zhong[szz]]，添加到values里面
                if szz in zhong.keys():
                    pass
                else:
                    zhong[n] = [szz]
                    n = n + 1
                out[zhong[n]].append(line[1])

            elif line[0] == 'deqteam':
                print(out[szz])
                out.pop(szz)

        except Exception:
            for i in range(1,n+1):
                if i in out.keys():
                    print(out[szz])

        print(zhong)









print(yuan)

