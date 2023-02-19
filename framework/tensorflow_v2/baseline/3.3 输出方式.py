# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# y_i \in [0,1] => sigmoid
a = tf.random.normal([10])
s = tf.sigmoid(a)
print(a)
print(s)

# y_i \in [0,1], \sum{y_i}=1 => softmax (将最大值放大)
logits = tf.random.uniform([1,10], minval=-2, maxval=2)
prob = tf.nn.softmax(logits)
print(logits)
print(prob)
print(tf.reduce_sum(prob, axis=1))

# y_i \in [-1,1] => tanh
t = tf.tanh(a)
print(t)
