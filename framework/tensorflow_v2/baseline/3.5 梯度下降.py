# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# GradientTape 梯度带
w = tf.constant(1.)
x = tf.constant(2.)
y = w*x
with tf.GradientTape(persistent=True) as tape: # persistent=True => 多次调用gradient()方法
    tape.watch([w]) # being traced by this tape.
    y2 = x*w
grad1 = tape.gradient(target=y,sources=[w])
grad2 = tape.gradient(target=y2,sources=[w])
print(grad1) # None
print(grad2)
print()

# 2nd-order 二阶求导
# GradientTape 梯度带
w = tf.Variable(initial_value=1.)
b = tf.Variable(initial_value=0.1)
with tf.GradientTape() as t1:
    with tf.GradientTape() as t2:
        tape.watch([w,b])
        y = x*w + b
    dy_dw, dy_db = t2.gradient(target=y, sources=[w,b])
d2y_dw2 = t1.gradient(target=dy_dw, sources=[w])
print(dy_dw)
print(dy_db)
print(d2y_dw2)
