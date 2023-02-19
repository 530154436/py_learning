#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
"""
import sys
str1 = sys.stdin.readline().strip()
str2 = sys.stdin.readline().strip()
letter_list = [chr(i) for i in range(65,91)]
print(letter_list)

str3 = ''
n = len(str2)
for i in range(0,n):
    k = letter_list.index(str2[i])
    str3 = str3 + letter_list[k-1]
print(str3)


line = datetime.strptime(line,"%Y-%m-%d")
out = datetime.strftime(line,"%m/%d/%Y")
print(out)



while True:
    n = sys.stdin.readline().strip()
    if not n:
        break
    n = int(n)
    Q = {1:{2},2:{3},3:{5}}
    Q1 = {2}
    Q2 = {3}
    Q3 = {5}

    if n==1:
        print(1)
    else:
        for i in range(2,n+1):
            min1 = min(Q[1])
            min2 = min(Q[2])
            min3 = min(Q[3])
            dic = {min1:1,min2:2,min3:3}
            min = min(min1,min2,min3)
            k = dic[min]
            Q[k].add(2*min,3*min,5*min)
            print(Q[k])


# 定义一个字典存储长度分别为1-30的单词
allz = {}
for i in range(1,31):
    allz[i] = []

# 把所有的单词按照长度分类
while True:
    line = sys.stdin.readline().strip()
    if line == '#':
        break
    sp = line.split(' ')
    for i in sp:
        l = len(i)
        allz[l].append(i)

# 定义文章中的特殊单词集合
jihe = []

# 按照单词长度遍历，查看是否有相同的单词
for key in allz.keys():
    ls = list(set(allz[key]))
    ls.sort(key = allz[key].index)
    print(ls)
    if ls == []:
        continue

    # 将所有的字母都转成大写
    res = [x.upper() for x in ls]

    for i in res:
        for j in res:
            if Counter(i) == Counter(j):
                jihe.append(i)
                break

print(jihe)