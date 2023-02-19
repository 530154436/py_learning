# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import numpy as np
import tensorflow as tf
from pathlib import Path
from tensorflow.python.keras import layers,optimizers,metrics,Sequential,models

tf.compat.v1.enable_eager_execution()   # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

def print_info(x, name=''):
    '''
    打印信息
    '''
    if isinstance(x, np.ndarray):
        print(f'ndarray: {name}.shape={x.shape}, type({name})={type(x)}, min({name})={x.min()}, max({name})={x.max()}')
    elif isinstance(x, tf.Tensor):
        print(f'Tensor: {name}.shape={x.shape}, {name}.dtype={x.dtype}')

def preprocess(x,y):
    x = tf.cast(x, dtype=tf.float32) / 255 - 1 # [0,255]=>[-1,1]
    x = tf.reshape(x, [28*28]) # (28,28) => (28*28)
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(tf.squeeze(y), depth=10) # 压缩维度1, [1,10] => [10]
    return x,y

# (60000, 28, 28), (60000,), (10000, 28, 28), (10000,)
(x,y), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train, x_val = tf.split(x, num_or_size_splits=[50000, 10000])
y_train, y_val = tf.split(y, num_or_size_splits=[50000, 10000])

db_train = tf.data.Dataset.from_tensor_slices((x_train,y_train))
db_train = db_train.map(preprocess).shuffle(10000).batch(128)

db_val = tf.data.Dataset.from_tensor_slices((x_val,y_val))
db_val = db_val.map(preprocess).shuffle(10000).batch(128)

db_test = tf.data.Dataset.from_tensor_slices((x_test,y_test))
db_test = db_test.map(preprocess).batch(128)

print_info(x_train, name='x_train')
print_info(y_train, name='y_train')
print_info(x_val, name='x_val')
print_info(y_val, name='y_val')
print_info(x_test, name='x_test')
print_info(y_test, name='y_test')

model = Sequential(name='linear_layer',
                   layers=[layers.Dense(units=256, activation=tf.nn.relu),  # [b,784] => [b,256]
                           layers.Dense(units=128, activation=tf.nn.relu),  # [b,256] => [b,128]
                           layers.Dense(units=64, activation=tf.nn.relu),  # [b,128] => [b,64]
                           layers.Dense(units=32, activation=tf.nn.relu),  # [b,64]  => [b,32]
                           layers.Dense(units=10, activation=tf.nn.relu)])  # [b,32]  => [b,10]
model.build(input_shape=(None, 28*28))
model.compile(optimizer=optimizers.Adam(lr=1e-3),
              loss=tf.compat.v2.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(db_train,
          epochs=5,
          validation_data=db_val, # 验证集
          validation_freq=2)      # 设置验证频率

model.evaluate(db_test)



