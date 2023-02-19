# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# Perceptron (单一输出节点感知机)
x = tf.random.normal([1,3])
w = tf.ones([3,1])
b = tf.ones([1])
y = tf.constant([1])

with tf.GradientTape() as tape:
    tape.watch([w,b])
    logits = tf.sigmoid(x@w+b)
    loss = tf.reduce_mean(tf.compat.v2.losses.MSE(y, logits))

grads = tape.gradient(loss, [w,b])
print('dy/dw=\n', grads[0]) # (3,1)
print('dy/db=\n', grads[1]) # (1,)
print()

# Multi-output Perceptron (多输出节点感知机)
x = tf.random.normal([2,4])
w = tf.ones([4,3])
b = tf.zeros([3])
y = tf.constant([2,0])

with tf.GradientTape() as tape:
    tape.watch([w,b])
    logits = x@w+b
    prob = tf.nn.softmax(logits, axis=-1)
    loss = tf.reduce_mean(tf.compat.v2.losses.MSE(tf.one_hot(y,depth=3), prob))

grads = tape.gradient(loss, [w,b])
print('dy/dw=\n', grads[0]) # (4,3)
print('dy/db=\n', grads[1]) # (3,)