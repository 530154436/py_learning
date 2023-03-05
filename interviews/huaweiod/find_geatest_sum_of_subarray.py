# -*- coding:utf-8 -*-
# 连续子数组的最大和
# 链接：https://www.nowcoder.com/questionTerminal/459bd355da1549fa8a49e350bf3df484
# 来源：牛客网
# 输入一个整型数组，数组里有正数也有负数。数组中的一个或连续多个整数组成一个子数组。求所有子数组的和的最大值。要求时间复杂度为 O(n).
# 示例1
# 输入
# [1,-2,3,10,-4,7,2,-5]
# 输出
# 18
# 说明
# 输入的数组为{1,-2,3,10,—4,7,2,一5}，和最大的子数组为{3,10,一4,7,2}，因此输出为该子数组的和 18。

import sys
class Solution:
    def FindGreatestSumOfSubArray(self, array):
        # write code here
        n = len(array)

        # 初始化二维数组: dp[i][j]表示 a[i]+...+a[j]
        dp = [[0] * n for _ in range(n)]

        # 动态规划
        max_sum = -sys.maxsize
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    dp[i][i] = array[i]
                else:
                    dp[i][j] = dp[i][j - 1] + array[j]
                if max_sum < dp[i][j]:
                    max_sum = dp[i][j]
        return max_sum

    def FindGreatestSumOfSubArray2(self, array):
        # 初始化一维数组:
        # dp[i] = dp[i-1]+array[i], dp[i-1]>0
        #       = array[i],         dp[i-1]<0 or i==0
        # 最终最大连续子数组和=max(dp[i])
        n = len(array)
        dp = [0] * n
        dp[0] = array[0]
        max_sum = array[0]
        for i in range(1,n):
            if dp[i-1]>0:
                dp[i] = dp[i-1]+array[i]
            else:
                dp[i] = array[i]
            if max_sum<dp[i]:
                max_sum = dp[i]
        return max_sum


if __name__ == '__main__':
    print(Solution().FindGreatestSumOfSubArray([1, -2, 3, 10, -4, 7, 2, -5]))
    print(Solution().FindGreatestSumOfSubArray2([1, -2, 3, 10, -4, 7, 2, -5]))
