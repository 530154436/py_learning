#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/03/15
@function:
"""
import sys

# https://www.nowcoder.com/practice/181a1a71c7574266ad07f9739f791506?tpId=37&tqId=21288&rp=1&ru=%2Fta%2Fhuawei&qru=%2Fta%2Fhuawei%2Fquestion-ranking&tab=answerKey
# https://www.cnblogs.com/fanguangdexiaoyuer/p/11281179.html

try:
    strings = []
    while True:
        str1 = sys.stdin.readline().strip()
        str2 = sys.stdin.readline().strip()
        if not str1 or not str2:
            break
        strings.append((str1, str2))

    for str1,str2 in strings:
        m, n = len(str1), len(str2)
        # 初始值均为0
        dp = [[0] * (n+1) for _ in range(m+1)]
        # 动态规划
        maxi, maxj = 1, 1
        for i in range(1, m+1):
            for j in range(1, n+1):
                if str1[i-1] == str2[j-1]:
                    # 初始化、递归
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = 0

                # 找到最长公共子串
                flag1 = dp[i][j] > dp[maxi][maxj]

                # 若有多个，输出在较短串中最先出现的那个。
                flag2 = (dp[i][j]==dp[maxi][maxj]) and ((m<n and i<maxi) or (m>n and j<maxj))

                if flag1 or flag2:
                    maxi = i
                    maxj = j

        start = maxi - dp[maxi][maxj] + 1
        print(str1[start-1:maxi])
except Exception as e:
    raise e


