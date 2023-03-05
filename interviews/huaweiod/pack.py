#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/13
@function:
"""
import sys
# ---------------------
# 简化示例-方便调试
# https://www.nowcoder.com/practice/f9c6f980eeec43ef85be20755ddbeaf4?tpId=37&tags=&title=&diffculty=0&judgeStatus=0&rp=1&tab=answerKey
# ---------------------
# 62
# 15 7
# 5 1 0
# 4 4 0
# 3 5 1
# 4 5 1
# 2 5 0
# 5 4 0
# 4 4 0
#
# 743
# 200 10
# 50 1 0
# 40 4 0
# 30 5 1
# 40 5 1
# 20 5 0
# 50 4 5
# 40 4 0
# 32 2 0
# 41 3 0
# 40 3 5
# ---------------------

while True:
    # 读数据
    line = sys.stdin.readline().strip()
    if not line:
        break
    line = line.split(' ')
    N, m = int(line[0]), int(line[1])
    dp = [[0] * (N + 1) for _ in range(61)] # m,N => m<=60,N<32000

    # 分组背包问题: 主件、主件+附件1、主件+附件2、主件+附件1+附件2
    v = [[0]*4 for _ in range(61)] # 价格 (m,4)
    w = [[0]*4 for _ in range(61)] # 重要度 (m,4)

    for i in range(1, m+1):
        line = sys.stdin.readline().strip()
        line = line.split(' ')
        vi,wi,pi = int(line[0]),int(line[1]),int(line[2]) # 价格、重要度、是否主件
        if pi==0: # 主件
            v[i][0] = vi
            w[i][0] = vi*wi # w*v
        else:
            if v[pi][1]==0:
                # 主件+附件1
                v[pi][1] = v[pi][0]+vi
                w[pi][1] = w[pi][0]+vi*wi  # w*v
            else:
                # 主件+附件2
                v[pi][2] = v[pi][0]+vi
                w[pi][2] = w[pi][0]+vi*wi  # w*v

                # 主件+附件1+附件2
                v[pi][3] = v[pi][1]+vi
                w[pi][3] = w[pi][1]+vi*wi  # w*v

    # for i in range(1,m+1):
    #     print(f'v{i}=',v[i])
    # for i in range(1,m+1):
    #     print(f'w{i}=',w[i])

    # 动态规划: 5种情况(主件、主件+附件1、主件+附件2、主件+附件1+附件2、全都不选)
    # for i in range(0,N+1):
    #     print(i, end='\t')
    # print()
    for i in range(1, m+1):
        for c in range(1, N+1):
            # 5种情况中取最大价值
            max_t = dp[i-1][c]
            for k in range(4):
                if v[i][k]<=c:
                    max_t = max(max_t, dp[i-1][c-v[i][k]]+w[i][k])
            dp[i][c] = max_t
        #
        # for item in dp[i]:
        #     print(item, end='\t')
        # print()
    print(dp[m][N])







