# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# 1. y    = f(x)  = xw+b
#    norm = ||x|| = \sum{x^2}       (L2正则化)
#    loss = \sum{{y-f(x)}^2}        (Mean Squared Error, 均方差)
#         = \sum{{y-(xw+b)}^2}
#         = norm(y-(xw+b))^2
#
#   => \partial{f_w(x)} / \partial{w} = x
#   => \partial{f_w(x)} / \partial{b} = 1
#   => \partial{loss} / \partial{w}   = \sum{2*[y-f_w(x)]*(-x)}
#   => \partial{loss} / \partial{b}   = \sum{2*[y-f_w(x)]*(-1)}
#
x = tf.ones([2,4])
w = tf.random.normal([4,3])
b = tf.zeros([3])
y = tf.constant([2, 0])

with tf.GradientTape() as tape:
    tape.watch([w,b])
    prob = tf.nn.softmax(x@w+b, axis=-1)

    # reduce_mean => 样本的平均误差
    loss = tf.reduce_mean(tf.compat.v2.losses.MSE(tf.one_hot(y, depth=3), prob))

grads = tape.gradient(target=loss, sources=[w,b])
print('d{loss}/dw = \n', grads[0]) # (4,3)
print('d{loss}/db = \n', grads[1]) # (3,)
print()

# 1. CrossEntropy Gradient
x = tf.ones([2,4])
w = tf.random.normal([4,3])
b = tf.zeros([3])
y = tf.constant([2, 0])

with tf.GradientTape() as tape:
    tape.watch([w,b])
    logits = x@w+b

    # reduce_mean => 样本的平均误差
    # tf.nn.softmax_cross_entropy_with_logits_v2
    loss = tf.reduce_mean(
        tf.compat.v2.losses.categorical_crossentropy(y_true=tf.one_hot(y, depth=3),
                                                     y_pred=logits,
                                                     from_logits=True))
grads = tape.gradient(target=loss, sources=[w,b])
print('d{loss}/dw = \n', grads[0]) # (4,3)
print('d{loss}/db = \n', grads[1]) # (3,)
print()