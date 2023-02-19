# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# 1. y = sigmoid(x)                     \in [0,1]
#      = 1/(1+e^{-x})
#
#    => dy/dx = e^{-x} / (1+e^{-x})^2
#             = (1+e^{-x}-1) / (1+e^{-x})^2
#             = 1/(1+e^{-x}) - 1/(1+e^{-x})^2
#             = sigmoid(x) - sigmoid^2(x)
#             = sigmoid(x) * (1-sigmoid(x))
#
#    => 缺点: 梯度弥散(x->+inf, dy/dx->0)
#
x = tf.linspace(start=-20., stop=20., num=10)
with tf.GradientTape() as tape:
    tape.watch(x)
    y = tf.sigmoid(x)
grads = tape.gradient(target=y, sources=[x])
print('sigmoid')
print('x\n',x)
print('y\n',y)
print('grads\n', grads)
print()

# 2. [x_1,...,x_n] =softmax=> [y_1,..,y_n]
#    y_i = e^{x_i} / \sum_{k=1}^{n}{e^{x_k}}
#
#    => max    : 非黑即白，最后的输出是一个确定的变量。
#       softmax: 分值大的一项被经常取到，而分值较小的那一项也有一定的概率偶尔被取到。
#
#    (1) j=i
#       => \partial{y_j}/\partial{x_i} = [e^{x_j}*\sum{e^{x_k}} - e^{x_i}*e^{x_j}] / [\sum{e^{x_k}}]^2
#                                      = [e^{x_j}*(\sum{e^{x_k}}-e^{x_i})] / [\sum{e^{x_k}}]^2
#                                      = e^{x_j}/\sum{e^{x_k}} * (\sum{e^{x_k}}-e^{x_i})/\sum{e^{x_k}}
#                                      = softmax(x_j) - (1-softmax(x_i))
#                                      = softmax(x_i) - (1-softmax(x_i))
#    (2) j!=i
#       => \partial{y_j}/\partial{x_i} = [0*\sum{e^{x_k}} - e^{x_i}*e^{x_j}] / [\sum{e^{x_k}}]^2
#                                      = - (e^{x_i}/\sum{e^{x_k}}) * (e^{x_j}/\sum{e^{x_k}})
#                                      = - softmax(x_i) * softmax(x_j)
#
x = tf.linspace(start=-1., stop=1., num=10)
with tf.GradientTape() as tape:
    tape.watch(x)
    y = tf.nn.softmax(x)
grads = tape.jacobian(target=y, sources=[x]) # (10,10)
print('softmax')
print('x\n',x)
print('y\n',y)
print('grads\n', grads)
print()

# 3. y = tanh(x) (双曲正切)             \in [-1,1]
#      = (e^x-e^{-x}) / (e^x+e^{-x})
#      = (1-e^{-2x}) / (1+e^{-2x})
#      = {2-(1+e^{-2x})} / (1+e^{-2x})
#      = 2/(1+e^{-2x}) - 1
#      = 2sigmoid(2x) - 1
#
#    => dy/dx = {(e^x+e^{-x})*(e^x+e^{-x}) - (e^x-e^{-x})*(e^x-e^{-x})} / (e^x+e^{-x})^2
#             = 1 - (e^x-e^{-x})^2/(e^x+e^{-x})^2
#             = 1 - tanh^2(x)
#
x = tf.linspace(start=-5., stop=5., num=10)
with tf.GradientTape() as tape:
    tape.watch(x)
    y = tf.tanh(x)
grads = tape.gradient(target=y, sources=[x])
print('tanh')
print('x\n',x)
print('y\n',y)
print('grads\n', grads)
print()

# 4. y = relu(x) = max(0,x)  (修正线性单元)
#
#    => dy/dx = 1 if(x>0) 0
#
#    => 保持梯度不变，不易出现梯度弥散或梯度爆炸
x = tf.linspace(start=-1., stop=1., num=10)
with tf.GradientTape() as tape:
    tape.watch(x)
    y = tf.nn.relu(x)
grads = tape.gradient(target=y, sources=[x])
print('relu')
print('x\n',x)
print('y\n',y)
print('grads\n', grads)
print()

# 5. y = leaky_relu(x)          (泄漏的修正线性单元)
#      = x,    if(x>=0)
#        x/a,  if(x<0),  a \in (1,+inf)
#
#    => dy/dx = 1 if(x>=0) 1/a
#
#    => 保持梯度不变，不易出现梯度弥散或梯度爆炸
#
x = tf.linspace(start=-1., stop=1., num=10)
with tf.GradientTape() as tape:
    tape.watch(x)
    y = tf.nn.leaky_relu(x)
grads = tape.gradient(target=y, sources=[x])
print('leaky_relu')
print('x\n',x)
print('y\n',y)
print('grads\n', grads)
print()
