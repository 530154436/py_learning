# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# pad 补齐
# paddings.shape=[n, 2] => n对应a的维度,2表示0(首位置)或-1(末位置)
a = tf.reshape(tf.range(9), shape=[3,3])
b = tf.pad(a, paddings=[[1,0],[0,0]], constant_values=0) # [4,3]=[3+1,3]
c = tf.pad(a, paddings=[[1,1],[0,1]], constant_values=0) # [5,4]=[3+1+1,3]

a1 = tf.range(9)
b1 = tf.pad(a1, paddings=[[0, 8]]) # (17,)

a2 = tf.random.normal([4,28,28,3])
b2 = tf.pad(a2, paddings=[[0, 8],[0,1],[1,1],[1,2]]) # (12, 29, 30, 6)
print(a)
print(b)
print(c)
print(a1)
print(b1)
print(a2.shape)
print(b2.shape)
print()

# tile 复制 => 所有维度
# The output tensor's i'th dimension has `input.dims(i) * multiples[i]` elements,
a = tf.reshape(tf.range(9), shape=[3,3])
b = tf.tile(a, multiples=[1,2]) # (3,6)
c = tf.tile(a, multiples=[2,2]) # 先复制小维度
d = tf.broadcast_to(tf.constant([[1,2,3]]), shape=(4,3)) # 运行时才自动拓展
print(a)
print(b)
print(c)
print(d)
print()