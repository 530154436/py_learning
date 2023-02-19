# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf
from tensorflow.python.keras import layers

tf.compat.v1.enable_eager_execution()   # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

x = tf.random.normal([1,32,32,3])
print(x.shape)

conv2d = layers.Conv2D(filters=4,           # 定义滤波器个数,决定了输出的通道数
                       kernel_size=(5,5),   # 卷积核大小
                       strides=1,           # 向右向下移动的步长
                       padding='valid')     # valid(丢) => out_height = ceil( float(in_height-filter_height+1) / stride_h)
                                            #              out_width = ceil( float(in_width - filter_width+1) / stride_w)
                                            # same(补)  => out_height = ceil( float(in_height) / stride_h)
                                            #              out_width = ceil( float(in_width) / stride_w)
