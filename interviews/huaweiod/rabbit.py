import sys

# ----------------------------------------------------------------
# https://www.nowcoder.com/practice/1221ec77125d4370833fd3ad5ba72395?tpId=37&tqId=21260&rp=1&ru=%2Fta%2Fhuawei&qru=%2Fta%2Fhuawei%2Fquestion-ranking&tab=answerKey
# 对于第i个月的兔子数量，由两部分组成:
#    一部分是上个月的兔子f(i-1)
#    另一部是满足2个月大的兔子，即 f(i-2)
#        从第3个月开始生1只兔子，即为新生兔子数量==满足2个月大的兔子数量
# ----------------------------------------------------------------
while True:
    line = sys.stdin.readline()
    if not line:
        break
    N = int(line.strip())
    dp = [0]*(N+1)
    dp[1] = 1
    dp[2] = 1
    for i in range(3, N+1):
        dp[i] = dp[i-1]+dp[i-2]
    print(dp[N])