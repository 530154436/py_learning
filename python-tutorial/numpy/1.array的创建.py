import numpy as np

'''
array：创建数组
dtype：指定数据类型
zeros：创建数据全为0
ones：创建数据全为1
empty：创建数据接近0
arrange：按指定范围创建数据
linspace：创建线段
'''

a = np.array([2,23,4],dtype=np.int)

# dtype: 数据类型
print(a.dtype)

# 矩阵
a = np.array([[2,23,4],
              [2,32,4]])
print(a)

# 创建全零数组
a = np.zeros((3,4))
print(a)

# 创建数据全为1
a = np.ones((3,4))
print(a)

# 创建连续数组: 10-19 的数据，2步长
a = np.arange(10, 20, 2)
print(a)

# 改变数据的形状
a = np.arange(12).reshape((3,4))
print(a)

# 创建全空数组, 其实每个值都是接近于零的数
a = np.empty((2,3)) # 数据为empty，3行4列
print(a)

# 创建线段
a = np.linspace(1,10,5)  # 开始端1，结束端10，且分割成5个数据，生成线段
print(a)