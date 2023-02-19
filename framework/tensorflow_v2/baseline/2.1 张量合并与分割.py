# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# concat 在原来的基础上进行合并 (除 $axis 的维度可以不等外其他维度必须相同)
# [class1-4, students, scores]
# [class5-6, students, scores]
a = tf.constant([1,2,3])
b = tf.constant([3,4,5])
print(a.shape, b.shape)
print(tf.concat(values=(a,b),axis=0)) # axi=1 => InvalidArgumentError: dimensions in the range [-1, 1)

a = tf.ones(shape=[4,35,8])
b = tf.ones(shape=[2,35,8])
c = tf.concat(values=(a,b), axis=0)
d = tf.concat(values=(a,a), axis=-1)
print(f'a={a.shape}')
print(f'b={b.shape}')
print(f'c={c.shape}')
print(f'd={d.shape}')

# stack 将秩为r的张量列表堆叠成一个秩为(r+1)的张量 (所有维度都必须相等)
# school1: [class, students, scores]
# school2: [class, students, scores]
# [schools, class, students, scores]
x = tf.constant([1, 4])
y = tf.constant([2, 5])
z = tf.constant([3, 6])
print(x.shape, y.shape, z.shape)
print(tf.stack([x, y, z]))  # [[1, 4], [2, 5], [3, 6]] (Pack along first dim.)
print(tf.stack([x, y, z], axis=1))  # [[1, 2, 3], [4, 5, 6]]

e = tf.stack(values=(a,a), axis=0)
f = tf.stack(values=(a,a), axis=3)
print(f'e={e.shape}')
print(f'f={f.shape}')

# unstack => 将value根据axis分解成num个张量，返回的值是list类型
a = tf.ones(shape=[4,35,8])
b = tf.ones(shape=[4,35,8])
c = tf.stack((a,b), axis=0)
tensors = tf.unstack(value=c, axis=0) # return 'list' object
print(a.shape, b.shape)
print(c.shape)
print(f'len(tensors)={len(tensors)}')
for i,tensor in enumerate(tensors):
    print(f'tensor{i}: {tensor.shape}')

# split 根据num_or_size_splits打散维度axis的数据
s = tf.split(c, axis=3, num_or_size_splits=2) # 8/4=num_or_size_split
print(f'len(s)={len(s)}')
for j,term in enumerate(s):
    print(f'tensor{j}: {term.shape}')

s = tf.split(c, axis=3, num_or_size_splits=[2,2,4]) # 2+2+4=8
print(f'len(s)={len(s)}')
for j,term in enumerate(s):
    print(f'tensor{j}: {term.shape}')