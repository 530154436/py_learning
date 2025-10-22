import numpy as np

A = np.arange(2,14).reshape(3,4)
# [[ 2  3  4  5]
#  [ 6  7  8  9]
#  [10 11 12 13]]

print(np.argmin(A))  # 0 -最小值的索引
print(np.argmax(A))  # 11 -最大值的索引

# 求矩阵均值
print(np.mean(A))
print(np.average(A))

# mean()函数还有另外一种写法
print(A.mean())
print(np.median(A))

# 累加函数
# 每一项矩阵元素均是从原矩阵首项累加到对应项的元素之和。
print(np.cumsum(A))  # [2 5 9 14 20 27 35 44 54 65 77 90]

# 累差运算函数
# 每一行中后一项与前一项之差
print(np.diff(A))

# 将所有非零元素的行与列坐标分割开，重构成两个分别关于行和列的矩阵。
print(np.nonzero(A))

# 排序
# 仅针对每一行进行从小到大排序操作
A = np.arange(14,2,-1).reshape((3,4))
print(np.sort(A))

# 矩阵的转置
print(np.transpose(A))
print(A.T)

# clip(Array,Array_min,Array_max) 剪裁
# if item < Array_min ---> item = Array_min
# if item > Array_max ---> item = Array_max
print(np.clip(A,5,9))


