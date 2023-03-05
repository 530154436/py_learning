#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/04/01
@function:
"""
# 链接：https://www.nowcoder.com/questionTerminal/2fb62a4500af4f4ba5686c891eaad4a9
# 给定一个 n * m 的矩阵 a，从左上角开始每次只能向右或者向下走，最后到达右下角的位置，
# 路径上所有的数字累加起来就是路径和，输出所有的路径中最小的路径和。
#
# 输入描述:
# 第一行输入两个整数 n 和 m，表示矩阵的大小。
# 接下来 n 行每行 m 个整数表示矩阵。
#
# 输出描述:
# 输出一个整数表示答案。
#
# 示例1
# 输入
# 4 4
# 1 3 5 9
# 8 1 3 4
# 5 0 6 1
# 8 8 4 0
#
# 输出
# 12
import sys

def min_path_sum(matrix, n, m):
    dp = [[0]*(m) for _ in range(n)]

    # 第1行赋初值
    for j in range(m):
        dp[0][j] = matrix[0][j] if j==0 else matrix[0][j] + dp[0][j-1]
    # 第1列赋初值
    for i in range(n):
        dp[i][0] = matrix[i][0] if i==0 else matrix[i][0] + dp[i-1][0]

    # 递归
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = min(dp[i][j-1], dp[i-1][j]) + matrix[i][j]

    return dp[n-1][m-1]

row1 = sys.stdin.readline()
row1 = row1.strip().split(' ')
n, m = int(row1[0]), int(row1[1])

matrix = []
for i in range(n):
    rowi = sys.stdin.readline().strip()
    matrix.append([ int(num) for num in rowi.split(' ')])

print(min_path_sum(matrix, n, m))
