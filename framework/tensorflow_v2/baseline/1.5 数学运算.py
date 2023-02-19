# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

# 1. element-wise: +-*/ 对应元素进行操作
a = tf.ones(shape=[2,2])
b = tf.fill(dims=[2,2], value=2.)
print(f'a={a}')
print(f'b={b}')
print(f'a+b={a+b}')
print(f'a-b={a-b}')
print(f'a*b={a*b}')
print(f'a/b={a/b}')
print(f'b//a={b//a}') # 整除
print(f'b%a={b%a}')   # 余除
print(f'log(a)={tf.math.log(a)}')
print(f'exp(a)={tf.math.exp(a)}')
print(f'log_2(8)={tf.math.log(8.)/tf.math.log(2.)}')       # 换底公式=>log2
print(f'log_10(100)={tf.math.log(100.)/tf.math.log(10.)}') # 换底公式=>log10
print(f'b^3={tf.pow(b,3)}') # x^3
print(f'b^3={b**3}')        # x^3
print(f'sqrt(b)={tf.sqrt(b)}')  #sqrt(x)
print()

# 2. matrix-wise: @ matmul => 矩阵运算
print(f'a@b={a@b}')
print(f'a*b={tf.matmul(a,b)}') # matrix multiply

a = tf.ones([4,2,3])     # [batch_size, row1, col1]
b = tf.fill([4,3,5], 2.) # [batch_size, row2, col2]
print(f'a={a.shape}')
print(f'b={b.shape}')
print(f'a@b ({(a@b).shape})')
print(f'a*b ({(tf.matmul(a,b)).shape}') # [batch_size, row1, col2]
x = tf.ones([4,2])
w = tf.ones([2,1])
b = tf.constant(0.1)
print(tf.matmul(x,w)+b)

# 3. dim-wise: reduce_mean/max/min/sum
