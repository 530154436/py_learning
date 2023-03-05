import sys
# https://www.nowcoder.com/practice/bfd8234bb5e84be0b493656e390bdebf?tpId=37&tqId=21284&rp=1&ru=%2Fta%2Fhuawei&qru=%2Fta%2Fhuawei%2Fquestion-ranking&tab=answerKey
# m个相同的苹果 放在n个相同的盘子里，f(i,j) 表示分法个数
# 数据范围：0<=m<=10，1<=n<=10。
# 初始值:
#  f(i,1)=1; f(1, j)=1; f(0,j)=1
# 递归关系:
# (1) i<j，必有空的盘子，则 f(i,j) = f(i,i)
# (2) i>=j
#     ① 如果有1个空盘子 f(i,j-1)
#     ② 如果没有空盘子,盘子决不能有空的，否则会与①重复，即每个盘子至少为1， f(i-j,j)
# (3) f(i,j)=f(i-j,j)+f(i,j-1)
#
# 7 3
# 预期输出: 8

while True:
    line = sys.stdin.readline()
    if not line:
        break
    line = line.strip().split(' ')
    m, n = int(line[0]), int(line[1])

    dp = [[0]*(n+1) for _ in range(m+1)]

    # 赋初值
    for j in range(1, n+1): # j \in [1,n]
        dp[0][j] = 1
        dp[1][j] = 1
    for i in range(m+1): # i \in [0,m]
        dp[i][1] = 1

    # 动态规划
    for i in range(2, m+1):
        for j in range(2, n+1):
            if i<j:
                dp[i][j] = dp[i][i]
            else:
                dp[i][j] = dp[i-j][j] + dp[i][j-1]
    print(dp[m][n])