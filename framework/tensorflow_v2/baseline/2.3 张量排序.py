# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

a = tf.random.shuffle(tf.range(5))
sa = tf.sort(a, direction='DESCENDING')
idx = tf.argsort(a, direction='DESCENDING')
print(a)
print(sa)
print(idx)

a = tf.random.uniform([3,3], maxval=10, dtype=tf.int32) # 均匀分布
aa = tf.sort(a) #默认最后一个维度排序、升序
idx = tf.argsort(a)
ad = tf.sort(a, direction='DESCENDING')
print(a)
print(aa)
print(idx)
print(ad)

res = tf.math.top_k(a, k=2) # 前k个最大
print(res)
print(res.values)   # 返回值
print(res.indices)  # 返回索引

# top-k accuracy
