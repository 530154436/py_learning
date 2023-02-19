# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# 向量范数
a = tf.ones([2,3])

# L2 范数
print('L2 范数')
print(tf.norm(a))
print(tf.sqrt(tf.reduce_sum(tf.square(a))))
print(tf.norm(a, ord=2))

print(tf.norm(a, ord=2, axis=0))
print(tf.norm(a, ord=2, axis=1))
print()

# L1 范数
print('L1 范数')
print(tf.norm(a, ord=1))
print(tf.norm(a, ord=1, axis=0))
print(tf.norm(a, ord=1, axis=1))
print()

# min/max/mean
a = tf.random.normal([4,10])
print(f'min={tf.reduce_min(a)}')
print(f'max={tf.reduce_max(a)}')
print(f'mean={tf.reduce_mean(a)}')
print(f'axi=1,min={tf.reduce_min(a, axis=1)}')
print(f'axi=1,max={tf.reduce_max(a, axis=1)}')
print(f'axi=1,mean={tf.reduce_mean(a, axis=1)}')
print()

# argmax/argmin
print(f'axis=1,argmax={tf.argmax(a, axis=1)}')
print(f'axis=1,argmin={tf.argmin(a, axis=1)}')
print()

# equal
a = tf.constant([1,2,3,4,5])
b = tf.range(5)
res = tf.equal(a,b)
print(res)
print(tf.reduce_sum(tf.cast(res, dtype=tf.int32)))
print()

# unique
a = tf.constant([4,2,2,4,3])
print(tf.unique(a))