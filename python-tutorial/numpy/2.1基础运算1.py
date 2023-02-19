import numpy as np

###  一维度的矩阵运算  ###
a = np.array([10,20,30,40])
b = np.arange(4)   #[0 1 2 3]

# 矩阵减法
d = a - b  #[10 19 28 37]
print(d)

# 矩阵加法
d = a + b
print(d)

# 矩阵点乘
d = a * b
print(d)

# 幂运算
d = b**2
print(d)

# 三角函数
d = 10 * np.sin(a)
print(d)

# 逻辑判断
d = b<3
print(d)

###  多维度的矩阵运算  ###
a = np.array([[1,1],[0,1]])
b = np.arange(4).reshape(2,2)   # [0, 1]
                                # [2, 3]
# 标准的矩阵乘法
d = np.dot(a,b)
print(d)
# 或
d = a.dot(b)
print(d)

# 生成一个2行4列的矩阵，且每一元素均是来自从0到1的随机数
a = np.random.random((2,4))

# 求和
print(np.sum(a))
# 最小值
print(np.min(a))
# 最大值
print(np.max(a))

# 需要对行或者列进行查找运算，就需要在上述代码中为 axis 进行赋值。
# 当axis的值为0的时候，将会以列作为查找单元，
# 当axis的值为1的时候，将会以行作为查找单元。
# 列求和
print(np.sum(a,axis=1))
# 列最小值
print(np.min(a,axis=1))
# 列最大值
print(np.max(a,axis=1))
