# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# Dense层
x = tf.random.normal([4,20])
net = tf.keras.layers.Dense(512,activation=None)
out = net(x) #logits
print(out.shape, type(out))
print(f'w.shape={net.kernel.shape}, b.shape={net.bias.shape}')

net = tf.keras.layers.Dense(10)
net.build(input_shape=(None,20))
print(f'w.shape={net.kernel.shape}, b.shape={net.bias.shape}')
out = net.call(x)
print(out.shape, type(out))

# multi-Layers
x = tf.random.normal([2,4])
model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='relu'), # param: 4*4+4=20
    tf.keras.layers.Dense(3, activation='relu'), # param: 4*3+3=15
    tf.keras.layers.Dense(2)                     # parma: 3*2+2=8
])
model.build(input_shape=[None, 4])
out = model.call(inputs=x)
print(model.summary())
print(out.shape)
for p in model.trainable_weights:
    print(p.name, p.shape)