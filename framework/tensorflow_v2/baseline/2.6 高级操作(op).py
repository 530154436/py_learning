# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
https://www.w3cschool.cn/tensorflow_python/tensorflow_python-led42j40.html
'''
import os
import tensorflow as tf
import matplotlib.pyplot as plt

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# 1. Where
a = tf.random.normal([3,3])
mask = a>0
bool_mask = tf.boolean_mask(tensor=a,mask=mask)
indices = tf.where(condition=mask)              # 拿到索引
gather = tf.gather_nd(a, indices=indices)       # 根据索引拿到相应的数据
print(a)
print(mask)
print(bool_mask)
print(indices)
print(gather)

A = tf.ones([3,3])
B = tf.zeros([3,3])
A_B = tf.where(condition=mask, x=A, y=B) # `x` (if true) or `y` (if false)
print(A_B)
print()

# scatter_nd 根据indices将updates散布到新的(初始为零)张量.
indices = tf.constant([[4],[3],[1],[7]])
updates = tf.constant([9,10,11,12])
shape = tf.constant([8])
scatter = tf.scatter_nd(indices=indices, updates=updates, shape=shape)
print(scatter) # [ 0 11  0 10  9  0  0 12], shape=(8,)

indices = tf.constant([[0],
                       [2]])
updates = tf.constant([[[5,5,5,5],
                       [6,6,6,6],
                       [7,7,7,7],
                       [8,8,8,8]],
                      [[5,5,5,5],
                       [6,6,6,6],
                       [7,7,7,7],
                       [8,8,8,8]]]
                      )
shape = tf.constant([4,4,4])
scatter = tf.scatter_nd(indices=indices, updates=updates, shape=shape)
print(scatter)
print()

# meshgrid => 3d坐标轴 [n,2]
def func(x):
    '''
    :param x: [b,2]
    :return:
    '''
    return tf.math.sin(x[...,0]) + tf.math.sin(x[...,1])

y = tf.linspace(start=-2.,stop=2,num=100)
x = tf.linspace(start=-2.,stop=2,num=100)
points_x, points_y = tf.meshgrid(x,y) #[5,5] [5,5]
points = tf.stack([points_x, points_y], axis=2) #[5,5,2]
z = func(points) # [5,5]

plt.figure('2d 函数值')
plt.imshow(z, origin='lower', interpolation='none')
plt.colorbar()

plt.figure('2d 等高线')
plt.contour(points_x, points_y, z)
plt.colorbar()
plt.show()
print(points_x.shape)
print(points_y.shape)
print(z.shape)
print(points.shape)