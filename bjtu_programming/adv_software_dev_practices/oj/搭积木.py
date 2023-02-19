#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
有编号为0-(N-1)的若干个积木块按编号从小到大的顺序排成一行，每个积木块所在的位置为其对应的编号。
一个机器人可以操纵这些积木块，机器人可以执行如下指令：
mv a on b
将a和b所在列中a、b之上的所有积木块恢复到其最初所在列顶端，然后将积木块a搁置在积木块b之上。
mv a ov b
将积木块a之上的所有积木块恢复到其最初所在列顶端，然后将积木块a放置在积木块b所在列顶端。
st a on b
将积木块b之上的所有积木块恢复到其最初所在列顶端，然后将积木块a及其上的所有积木放置在积木块b之上。
st a ov b
将积木块a及其上的所有积木放置在积木块b所在列的顶端。
xh a an b
交换a和b所在的列。
q
退出
上述命令中，若存在a==b或a、b在同一列上，则为非法指令。机器人会忽略所有的非法指令，不会操作任何的积木块。
输入
输入的第一行为一个整数n(0<n<25)，随后有若干行指令，保证所有的指令为上述形式。若指令为q，表示指令结束。
输出
请输出机器人执行所有的指令后的积木状态。记机器人操作之前每个积木所在的列为i(0≤i<n)，请按样例形式输出每列的所有积木。
对任何一列，在一行中输出该列中所有的积木信息。输出格式为：
先输出列号和：，若该列无积木，则直接换行，否则在单个空格后输出各个积木块的编号，编号之间以单个空格分隔。
示例输入
10
mv 9 on 1
mv 8 ov 1
mv 7 ov 1
mv 6 ov 1
st 8 ov 6
st 8 ov 5
mv 2 ov 1
mv 9 on 8
mv 4 ov 9
xh 4 an 1
q
示例输出
0: 0
1: 5 8 9 4
2: 2
3: 3
4:
5: 1
6: 6
7: 7
8:
9:
"""
import sys

num = sys.stdin.readline().strip()
coordinate = {}
tamu = {}
for i in range(0,int(num)):
    coordinate[i] = [1,i]
    tamu[i] = [i]

while True:
    line = sys.stdin.readline().strip()
    if line == 'q':
        break
    line = line.split(' ')
    a = int(line[1])
    b = int(line[3])
    if a == b:
        continue
    la = coordinate[a][1]
    ha = coordinate[a][0]
    lb = coordinate[b][1]
    hb = coordinate[b][0]
    if la == lb:
        continue

    if line[0] == 'mv':
        # 清空a所在列上方的积木
        if ha == 1:
            pass
        else:
            for i in tamu[la][ha:]:
                tamu[la].remove(i)
                tamu[i].append(i)
                coordinate[i] = [len(tamu[i]), i]

        if line[2] == 'on':
            # 清空b所在列上方的积木
            if hb == 1:
                pass
            else:
                for j in tamu[lb][hb:]:
                    tamu[lb].remove(j)
                    tamu[j].append(j)
                    coordinate[j] = [len(tamu[j]),j]

         # 把a放到b列上
        tamu[lb].append(a)
        coordinate[a] = [len(tamu[lb]),lb]
        tamu[la].remove(a)

    elif line[0] == 'st':
        if line[2] =='on':
        # 清空b所在列上方的积木
            if hb == 1:
                pass
            else:
                for j in tamu[lb][hb:]:
                    tamu[lb].remove(j)
                    tamu[j].append(j)
                    coordinate[j] = [len(tamu[j]), j]

        # 把a和a所在列上方的积木放到b上方
        for i in tamu[la][ha-1:]:
            tamu[lb].append(i)
            coordinate[i] = [len(tamu[lb]),lb]
            tamu[la].remove(i)

    elif line[0] == 'xh':
        k = tamu[la]
        tamu[la] = tamu[lb]
        tamu[lb] = k

        for i in tamu[lb]:
            coordinate[i][1] = lb
        for j in tamu[la]:
            coordinate[j][1] = la

for k, v in tamu.items():
    if len(v) == 0:
        print(f'{k}:')
    else:
        print(f'{k}:', ' '.join(str(i) for i in v))