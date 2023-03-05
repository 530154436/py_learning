#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/17
@function:
"""
# 题目描述
# Levenshtein 距离，又称编辑距离，指的是两个字符串之间，由一个转换成另一个所需的最少编辑操作次数。
# 许可的编辑操作包括将一个字符替换成另一个字符，插入一个字符，删除一个字符。
# 编辑距离的算法是首先由俄国科学家Levenshtein提出的，故又叫Levenshtein Distance。
# Ex：
# 字符串A:abcdefg
# 字符串B: abcdef
#
# 通过增加或是删掉字符”g”的方式达到目的。这两种方案都需要一次操作。把这个操作所需要的次数定义为两个字符串的距离。
#
# 要求：
# 给定任意两个字符串，写出一个算法计算它们的编辑距离。
# 本题含有多组输入数据。
#
# 输入描述:
# 每组用例一共2行，为输入的两个字符串
#
# 输出描述:
# 每组用例输出一行，代表字符串的距离
#
# 示例1
# 输入
# abcdefg
# abcdef
# abcde
# abcdf
# abcde
# bcdef
#
# 输出
# 1
# 1
# 2
'''
    https://www.cxyxiaowu.com/10220.html  类似最长公共子序列
    https://www.cnblogs.com/yulinfeng/p/7096882.html
    定义：S1、S2表示两个字符串，S1(i)表示S1的第一个字符，d[i, j]表示S1的第i个前缀到S2的第j个前缀
    例如:S1 = ”abc”,S2 = ”def”,求解S1到S2的编辑距离为d[3, 3]）。
        若S1 = ”abc”, S2 = ”dec”，此时它们的编辑距离为d[3, 3] = 2，观察两个字符串的最后一个字符是相同的，
        也就是说S1(3) = S2(3)不需要做任何变换，故S1 = ”abc”, S2 = ”dec” <= > S1’ = ”ab”, S2’ = ”de”，
        即当S1[i] = S[j]时，d[i, j] = d[i-1,j -1]。
        得到公式：d[i, j] = d[i - 1, j - 1] (S1[i] = S2[j])
　　
    上面一条得出了当S1[i] = S2[j]的计算公式，显然还有另一种情况就是S1[i] ≠ S2[j]。
    若S1 = ”abc”, S2 = ”def”。S1变换到S2的过程可以“修改”，但还可以通过“插入”、“删除”使得S1变换为S2。
　　　　1)在S1字符串末位插入字符“f”，此时S1 = ”abcf”，S2 = ”def”,
        此时即S1[i] = S2[j]的情况，S1变换为S2的编辑距离为d[4, 3] = d[3, 2]。
        所以得出d[i, j]=d[i, j - 1] + 1。（+1是因为S1新增了”f”）
　　　　2)在S2字符串末位插入字符“c”，此时S1 = ”abc”，S2 = ”defc”，
        此时即S1[i] = S[j]的情况，S1变换为S2的编辑距离为d[3, 4] = d[2, 3]。
        所以得出d[i, j]=d[i - 1, j] + 1，实际上这是对S1做了删除。（+1是因为S2新增了”c”）
　　　　3)将S1字符串末位字符修改为”f”，此时S1 = ”abf”，S2 = ”def”，
        此时即S1[i] = S[j]的情况，S1变换为S2的编辑距离为d[3, 3] = d[2, 2]。
        所以得出d[i, j] = d[i – 1, j - 1] + 1。（+1是因为S1修改了“c”）

　　综上，得出递推公式：
     动态规划——字符串的编辑距离
     s1 = "abc", s2 = "def"
     计算公式：
              | 0                                           i = 0, j = 0
              | j                                           i = 0, j > 0
     d[i,j] = | i                                           i > 0, j = 0
              | d[i-1,j-1])                                 s1(i) = s2(j)
              | min(d[i,j-1]+1, d[i-1,j]+1, d[i-1,j-1]+1)   s1(i) ≠ s2(j)
     定义二维数组[4][4]：
         d e f            d e f
       |x|x|x|x|        |0|1|2|3|
     a |x|x|x|x|  =>  a |1|1|2|3|  => 编辑距离d = [4][4] = 3
     b |x|x|x|x|      b |2|2|2|3|
     c |x|x|x|x|      c |3|3|3|3|
 '''

import sys

def levenshtein_distance(str1, str2):
    m,n = len(str1), len(str2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    # 赋初值
    for i in range(1, m+1):
        dp[i][0] = i
    for j in range(1, n+1):
        dp[0][j] = j
    # 动态规划
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1]==str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+1)
    return dp[m][n]

try:
    lines = []
    while True:
        line1 = sys.stdin.readline().strip()
        line2 = sys.stdin.readline().strip()
        if not line1:
            break
        lines.append((line1, line2))
    for str1, str2 in lines:
        print(levenshtein_distance(str1, str2))
except Exception as e:
    raise e