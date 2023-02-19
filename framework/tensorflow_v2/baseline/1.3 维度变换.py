# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# Reshape
a = tf.random.normal(shape=[4,28,28,3])     # [b,height,width,chanel]
b = tf.reshape(tensor=a,shape=[4,784,3])    # [b,pixel,c]
c = tf.reshape(tensor=a,shape=[4,-1,3])     # [b,pixel,c] -1=>自动计算
d = tf.reshape(tensor=a,shape=[4,28*28*3])  # [b,data point]
e = tf.reshape(tensor=a,shape=[4,-1])       # [b,data point]
f = tf.reshape(tensor=a,shape=[-1])
print(a.shape, a.ndim)
print(b.shape, b.ndim)
print(c.shape, c.ndim)
print(d.shape, d.ndim)
print(e.shape, e.ndim)
print(f.shape, f.ndim)
print()

# transpose # 交换轴
a = tf.random.normal(shape=[4,3,2])
b = tf.transpose(a)
c = tf.transpose(a, perm=[0,2,1])   # 交换1、2轴 (转置)
print(a.shape)
print(b.shape)
print(c.shape)
print()

# Squeeze VS Expand_dims 降维/升维
# a: [classes, students, subjects] => add school dim
a = tf.random.normal([4,35,8])
b = tf.expand_dims(input=a, axis=0)
b1 = tf.expand_dims(input=a, axis=-4) # -4 [0 1 2] -1
c = tf.expand_dims(input=a, axis=3)
c1 = tf.expand_dims(input=a, axis=-1)
print(a.shape)
print(b.shape)
print(b1.shape)
print(c.shape)
print(c1.shape)

d = tf.squeeze(input=b, axis=0)
print(d.shape)

