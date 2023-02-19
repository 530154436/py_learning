# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import numpy as np
import tensorflow as tf
tf.compat.v1.enable_eager_execution()

os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# 创建常量
a = tf.constant(1,    dtype=tf.int32)
b = tf.constant(2.0,  dtype=tf.double)
c = tf.constant(True, dtype=tf.bool)
d = tf.constant('hi', dtype=tf.string)

print(a.dtype, '\t', a)
print(b.dtype, '\t', b)
print(c.dtype, '\t', c)
print(d.dtype, '\t', d)
print(isinstance(a, tf.Tensor))
print(tf.is_tensor(a))
print(a.dtype == tf.int32)
print()


# Tensor 属性
with tf.device('cpu'): a=tf.ones([3,4,2])
with tf.device('cpu'): b=tf.range(4)

print(a.device)
print(b.device)

print(b.numpy())
print(b.ndim)
print(tf.rank(b))
print(tf.rank(a))
print()
# print(b.name) # Tensor.name is meaningless when eager execution is enabled.

# 数据转换
a = np.arange(5)
print(a.dtype)
print(tf.convert_to_tensor(a))
print(tf.convert_to_tensor(a, dtype=tf.double))
print(tf.cast(a, dtype=tf.float32))

b = tf.constant([0,1])
c = tf.constant([False, True])
print(tf.cast(b, dtype=tf.bool))
print(tf.cast(c, dtype=tf.int32))
print()

# 变量
a = tf.Variable(tf.range(5))
print(a)
print(a.dtype)
print(a.name)
print(a.trainable)
print(isinstance(a, tf.Tensor))
print(isinstance(a, tf.Variable))
print(tf.is_tensor(a))
# Tensor => numpy
print(a.numpy())
print()

# 创建Tensor
a = tf.convert_to_tensor(value=np.ones([2,3]))
b = tf.convert_to_tensor(value=[1,2])
c = tf.convert_to_tensor(value=[[1.],[2]])
print(a)
print(b)
print(c)
print()

a = tf.zeros(shape=[])
b = tf.zeros(shape=[2,2])
c = tf.zeros(shape=[1,2,3]) # []从外到里
d = tf.zeros(c.shape)
e = tf.zeros_like(c) # <==> tf.zeros(c.shape)
print(a)
print(b)
print(c)
print(d)
print(e)
print()

a = tf.ones(shape=1)
b = tf.ones(shape=[2,2])
c = tf.ones(shape=[1,2,3]) # []从外到里
d = tf.ones(c.shape)
e = tf.ones_like(a) # <==> tf.ones(c.shape)
print(a)
print(b)
print(c)
print(d)
print(e)
print()

# 填充
a = tf.fill(dims=[2,2], value=9)
print(a)

# 随机化初始化
a = tf.random.normal(shape=[2,3], mean=0, stddev=1)           # 产生正态分布随机数(均值、标准差)
b = tf.random.truncated_normal(shape=[2,2], mean=0, stddev=1) # 产生截断正态分布随机数 => 防止梯度消失
c = tf.random.uniform(shape=[5], minval=0, maxval=1)          # 均匀分布随机采样

# Random Permutation
idx = tf.random.shuffle(value=tf.range(5))       # 随机打散
e = tf.gather(params=c,indices=idx)              # 根据索引数组随机打乱c
print(a)
print(b)
print(c)
print(d)
print(e)
print()

# 计算Loss
y_pred = tf.random.uniform(shape=[4, 5])
y_true = tf.range(4)
y_true = tf.one_hot(y_true, depth=5)
mse_loss = tf.keras.losses.mse(y_true, y_pred) # np.sum((y_pred-y_true)**2)/5
loss = tf.reduce_mean(mse_loss)                # np.mean(mse_loss)
print(y_true)
print(y_pred)
print(mse_loss)
print(loss)
print()

# Vector、Matrix - Dense
x = tf.random.normal([4,6])
net = tf.keras.layers.Dense(units=5)
net.build(input_shape=(4,6))    # (4,6) => (6,5)
y = net(x)
print(net)
print(f"x = {x.shape}")             # (4, 6)
print(f"w = {net.kernel.shape}")    # (6, 5)
print(f"b = {net.bias.shape}")      # (5,)
print(f"y = xw + b = {y.shape}")
print()

# Dim=3 Tensor
# x: [b, seq_len, word_dim] => [批大小, 句子长度, 词向量维度]
# (x_train, y_train), (x_test, y_test) = \
#     tf.keras.datasets.imdb.load_data(num_words=20)
# x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, maxlen=10)
# emb = embedding(x_train) # [25000,10,100]
# print(x_train.shape)
print()

# Dim=4 Tensor (卷积层)
# [b, h, w, c] => [批大小, 高度, 宽度， RGB]
x = tf.random.normal((4,2,2,3))
net = tf.keras.layers.Conv2D(16, kernel_size=3)
y = net(x)
print(x.shape)
print(y.shape)
