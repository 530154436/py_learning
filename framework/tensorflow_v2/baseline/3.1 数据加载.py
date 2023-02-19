# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# keras.datasets
def preprocess(x,y):
    x = tf.cast(x, dtype=tf.float32)/255.0
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    return x, y

# mnist
(x,y),(x_test, y_test) = tf.keras.datasets.mnist.load_data()
y_one_hot = tf.one_hot(y, depth=10)
y_test_one_hot = tf.one_hot(y_test, depth=10)
print(x.shape, y.shape)
print(x_test.shape, y_test.shape)
print(f'min(x),max(x),mean(x)={x.min()},{x.max()},{x.mean()}')
print(f'min(y),max(y),mean(y)={y.min()},{y.max()},{y.mean()}')

db = tf.data.Dataset.from_tensor_slices((x_test,y_test))
db = db.map(preprocess)
db = db.shuffle(10000).batch(100)
db_iter = iter(db)


# CIFAR10/100
# (x,y),(x_test, y_test) = tf.keras.datasets.cifar10.load_data()
# db = tf.data.Dataset.from_tensor_slices(x_test)
# print(x.shape, y.shape)
# print(x_test.shape, y_test.shape)