# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

def himmelblau(x):
    return (x[0] ** 2 + x[1] - 11) ** 2 + (x[0] + x[1] ** 2 - 7) ** 2

def plot_func():
    x = np.arange(-6, 6, 0.1)
    y = np.arange(-6, 6, 0.1)
    X,Y = np.meshgrid(x,y)
    Z = himmelblau([X,Y])
    print(f'x,y,z shape: {x.shape},{y.shape},{Z.shape}')

    fig = plt.figure('himmelblau')
    ax = fig.gca(projection='3d')
    ax.plot_surface(X,Y,Z)
    ax.view_init(60, -30)
    ax.set_xlabel('x')
    ax.set_xlabel('y')
    plt.show()

# plot_func()
# x = tf.constant([-4., 0.]) # 初始点: x0,y0 => 最优解: [-3.7793102 -3.283186 ]
x = tf.constant([5.,1.]) # 初始点: x0,y0  => 最优解: [3. 1.9999999]
for step in range(200):

    with tf.GradientTape() as tape:
        tape.watch([x])
        y = himmelblau(x)
    grads = tape.gradient(y, [x])[0]
    print(f'x={x}')
    print(f'y={y}')
    print(f'grads={grads}\n')
    # 梯度下降
    x -= 0.01*grads