# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# 大维度【4,16,16,32】 => 小维度 在小维度(右)对齐、无或1维自动扩展
a = tf.random.normal(shape=[4,5,2,3])
b = tf.random.normal(shape=[3])
c = tf.random.normal(shape=[5,2,1])
d = tf.random.normal(shape=[4,1,1,1])
print(f'shape(a) = {a.shape}')
print(f'shape(b) = {b.shape}')
print(f'shape(c) = {c.shape}')
print(f'shape(d) = {d.shape}')
print(f'shape(a+b) = {(a + b).shape}')
print(f'shape(a+c) = {(a + c).shape}')
print(f'shape(a+d) = {(a + d).shape}')
print()

# broadcast VS tile
a = tf.ones([3,4])
a1 = tf.broadcast_to(a, shape=[2,3,4])
a2 = tf.expand_dims(a, axis=0)          # 维度拓展
a3 = tf.tile(a2, multiples=[2,1,1])     # 复制: i'th dimension = `input.dims(i) * multiples[i]`
print(f'a={a.shape} =broadcast_to=> a1={a1.shape}')
print(f'a={a.shape} =expand_dims=> a2={a2.shape} =tile=> a3={a3.shape}')

