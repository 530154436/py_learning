# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# clip_by_value 根据值裁剪
a = tf.range(9)
b = tf.maximum(a, 2) # x > y ? x : y
b1 = tf.nn.relu(a)
c = tf.minimum(a, 8) # x < y ? x : y
d = tf.clip_by_value(a, 2, 8) # min(8, max(x,2)) --> 2<=x<=8
print(a)
print(b)
print(b1)
print(c)
print(d)
print()

# clip_by_norm 根据范数裁剪 => 等比例放缩(t * clip_norm / l2norm(t))
a = tf.random.normal([2,2],mean=10)
l2_a = tf.norm(a)
aa = tf.clip_by_norm(a, 15)
l2_aa = tf.norm(aa)
print(a)
print(l2_a)
print(aa)
print(l2_aa)
print()

# Gradient clipping 梯度裁剪 (tf.clip_by_global_norm)
(x,y),_ = tf.keras.datasets.mnist.load_data()
x = tf.convert_to_tensor(x, dtype=tf.float32)

print(x.shape)
print(y.shape)





