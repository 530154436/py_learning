# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# MSE = 1/N \sum{y-y_out}^2
# L2-norm = \sqrt{ \sum{y-y_out}^2 }
logits = tf.constant([1, 2, 3, 0, 2])
logits = tf.one_hot(logits, depth=4)
logits = tf.cast(logits, dtype=tf.float32)
y = tf.random.normal([5, 4])

loss1 = tf.reduce_mean(tf.square(logits - y))
loss2 = tf.square(tf.norm(logits - y)) / (5 * 4)
loss3 = tf.reduce_mean(tf.losses.mean_squared_error(labels=y, predictions=logits))
print(logits)
print(loss1)
print(loss2)
print(loss3)
print()

# 熵 越大越混乱，越不稳定，携带的信息就越少
# Categorical Cross Entropy 交叉熵, logits=>CrossEntropy
loss1 = tf.keras.losses.categorical_crossentropy(y_true=[0,1,0,0],y_pred=[0.25,0.25,0.25,0.25])
loss2 = tf.keras.losses.categorical_crossentropy(y_true=[0,1,0,0],y_pred=[0.25,0.5,0.05,0.20])
loss3 = tf.keras.losses.categorical_crossentropy(y_true=[0,1,0,0],y_pred=[0.1,0.7,0.1,0.1])
print(loss1)
print(loss2)
print(loss3)

loss1 = tf.keras.losses.binary_crossentropy(y_true=[1],y_pred=[0.1])
loss2 = tf.keras.losses.binary_crossentropy(y_true=[1],y_pred=[0.6])
print(loss1)
print(loss2)
print()

# 数值不稳定问题
x = tf.random.normal([1,500])
w = tf.random.normal([500,2])
b = tf.random.normal([2])

logits = x@w + b
prob = tf.nn.softmax(logits)
loss1 = tf.keras.losses.categorical_crossentropy([0,1],logits,from_logits=True) # 推荐True
loss2 = tf.keras.losses.categorical_crossentropy([0,1], prob) # 这种写法会出现数值稳定
print(f'logits={logits}')
print(f'prob={prob}')
print(f'loss1={loss1}')
print(f'loss2={loss2}')