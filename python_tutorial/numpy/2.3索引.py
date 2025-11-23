import numpy as np

A = np.arange(3,15).reshape((3,4))
# [[ 3  4  5  6]
#  [ 7  8  9 10]
#  [11 12 13 14]]
print(A)

# 第二行
print(A[2])
print(A[2,:])

# 第一列
print(A[:,1])

print(A[1,2])
print(A[1][2])

# 迭代行
for row in A:
    print(row)

# 迭代列
for col in A.T:
    print(col)

# 迭代元素
# flatten() 将多维的矩阵进行展开成1行的数列。
print(A.flatten())
# flat: 迭代器
for item in A.flat:
    print(item)

m,n = np.shape(A)
for i in range(m):
    for j in range(n):
        print(A[i,j])

