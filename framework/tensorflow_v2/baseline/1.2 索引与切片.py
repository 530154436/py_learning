# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# indexing
a = tf.ones([3,5,5,3])
print(a[0][0])  # (5,3)
print(a[0][0][0])   #(3,)
print(a[0][0][0][2]) # ()

# Numpy-stype indexing
print(a[1].shape) # (5, 5, 3)
print(a[1,2].shape) # (5, 3)
print(a[1,2,3].shape)  # (3, )
print(a[1,2,3,2].shape) # ()
print()

# 切片 start:end [A,B) => Vector
a = tf.range(10)
print(a)
print(a[-1:])
print(a[-2:])
print(a[:2])
print(a[:-1])
print(a[::-1])
print(a[::-2])
print(a[2::-2]) # [2 0] => 开始位置 右->左
print()

# index by :
a = tf.ones([3,5,5,3])
print(a.shape)
print(a[0,:,:,:].shape)
print(a[:,0,:,:].shape)
print(a[:,:,0,:].shape)
print(a[:,:,:,1].shape)

# start:end:step
print(a[0:2,:,:,:].shape)
print(a[:,:4:2,:,:].shape)
print()

# ...
a = tf.ones([3,5,5,3])
print(a[0, ...].shape)
print(a[..., 0].shape)
print(a[1,0,...,0].shape)
print()

# Selective Indexing

# tf.gather 收集某个维度数据
# data: [classes, students, subjects]
a = tf.ones([4,35,8])
b = tf.gather(a, axis=0, indices=[2,3]) # 2、3 class
c = tf.gather(a, axis=1, indices=[2,3,7,9,16])
d = tf.gather(a, axis=2, indices=[2,3,7])
print(a.shape)
print(b.shape)
print(c.shape)
print(d.shape)
print()

# tf.gather_nd 同时收集多个维度数据
# [class1 student1, class2 student2]
b = tf.gather_nd(a, indices=[0])  # => a[0] = (35,8)
c = tf.gather_nd(a, indices=[0,1])  # => a[0,1] = (8,)
d = tf.gather_nd(a, indices=[0,1,2])  # => a[0,1,3] = ()
e = tf.gather_nd(a, indices=[[0,1,2]]) # => [a[0,1,2]] = (1,)
f = tf.gather_nd(a, indices=[[0,0],[1,1]]) # => [a[0,0], a[1,1]] = (2,8)
g = tf.gather_nd(a, indices=[[[0,0,0], [1,1,1]]]) # => [[a[0,0,0] a[1,1,1]]] = (1,2)
print(b.shape)
print(c.shape)
print(d.shape)
print(e.shape)
print(f.shape)
print(g.shape)
print()

# tf.boolean_mask
a = tf.ones([2,3,4])
print(a.shape)
print(tf.boolean_mask(a, axis=0, mask=[True,False]).shape)
print(tf.boolean_mask(a, axis=1, mask=[True, True,False]).shape)
print(tf.boolean_mask(a, mask=[[True, False, False], [False,True,True]]).shape) # (3, 4) = (N,4)
print()