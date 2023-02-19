# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf

tf.compat.v1.enable_eager_execution()
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error

'''
    out = relu{ relu{ relu[ X@W1 + b1 ]@W2 + b2 }@W3 + b3 }
    pred = argmax(out)
    loss = MSE(out, label)
'''
# x : [60k, 28, 28] [10k, 28, 28] =type=> numpy.ndarray
# y : [60k] [10k]
(x, y), (x_test,y_test) = tf.keras.datasets.mnist.load_data()

# np.ndarry => tensor
x = tf.convert_to_tensor(value=x, dtype=tf.float32) / 255.   # 归一化，加快收敛速度
y = tf.convert_to_tensor(value=y, dtype=tf.int32)
x_test = tf.convert_to_tensor(value=x_test, dtype=tf.float32) / 255.   # 归一化，加快收敛速度
y_test = tf.convert_to_tensor(value=y_test, dtype=tf.int32)
print(x.shape, x.dtype, tf.reduce_min(x), tf.reduce_max(x))
print(y.shape, y.dtype, tf.reduce_min(y), tf.reduce_max(y))
print(x_test.shape, x_test.dtype)
print(y_test.shape, y_test.dtype)

# 取一个批次
train_db = tf.data.Dataset.from_tensor_slices(tensors=(x,y)).batch(128)
test_db = tf.data.Dataset.from_tensor_slices(tensors=(x_test,y_test)).batch(128)

train_iter = iter(train_db)
sample = next(train_iter)
print(f'batch: {sample[0].shape}, {sample[0].shape}')

# 裁剪过的正态分布 Variable可跟踪偏导
# [b,784] => [b,256] => [b,128] => [b,10]
# [dim_in, dim_out], [dim_out]
w1 = tf.Variable(name='w1', initial_value=tf.random.truncated_normal(shape=[784, 256],stddev=0.1))
b1 = tf.Variable(name='b1', initial_value=tf.zeros(shape=[256]))
w2 = tf.Variable(name='w2', initial_value=tf.random.truncated_normal(shape=[256, 128],stddev=0.1))
b2 = tf.Variable(name='b2', initial_value=tf.zeros(shape=[128]))
w3 = tf.Variable(name='w3', initial_value=tf.random.truncated_normal(shape=[128, 10],stddev=0.1))
b3 = tf.Variable(name='b3', initial_value=tf.zeros(shape=[10]))
lr = 1e-3

# 优化器
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)

# h1 = x@w1 + b1
for epoch in range(2): # 对整个数据集迭代

    total_correct,total_sum = 0, 0
    for step,(x,y) in enumerate(train_db): # 对每个批次迭代
        # x:[128, 28, 28]
        # y:[128]
        # [b, 28, 28] => [b, 28*28]
        x = tf.reshape(x, [-1, 28*28]) # [128,784]

        # 计算梯度 => 相当于计算偏导数 \partial{loss}/\partial{w_i}
        with tf.GradientTape() as tape: # 跟踪 tf.Variable
            # x:  [b, 28*28]
            # w1: [784, 256]
            # h1: [b, 256]
            h1 = tf.matmul(x, w1) + b1
            h1 = tf.nn.relu(h1)
            # h2 : [b,128]
            h2 = tf.matmul(h1, w2) + b2
            h2 = tf.nn.relu(h2)
            # h2 : [b,10]
            out = tf.matmul(h2, w3) + b3

            # loss
            # out: [b,10]
            # y: [b]
            y_one_hot = tf.one_hot(y, depth=10)

            # mse = mean(sum(y-out)^2)
            # [b,10] => mean: scalar 标量
            loss = tf.reduce_mean(tf.square(y_one_hot-out))

        # 计算梯度 => loss:nan (梯度爆炸) => 改变初始值
        grads = tape.gradient(target=loss, sources=[w1,w2,w3,b1,b2,b3])
        # w1 = w1 - lr * w1_grad <= 梯度下降
        # w1.assign_sub(lr * grads[0]) # 原地更新
        # w2.assign_sub(lr * grads[1])
        # w3.assign_sub(lr * grads[2])
        # b1.assign_sub(lr * grads[3])
        # b2.assign_sub(lr * grads[4])
        # b3.assign_sub(lr * grads[5])

        # 自动更新参数
        optimizer.apply_gradients(grads_and_vars=zip(grads, [w1,w2,w3,b1,b2,b3]))

        if step % 100 == 0:
            print(f'epoch:{epoch},step:{step}, loss:{float(loss)}')

    # tes/evaluation
    for step, (x_,y_) in enumerate(test_db):
        # [b, 28, 28] => [b, 28*28]
        x_ = tf.reshape(x_, [-1, 28 * 28])  # [128,784]

        # [b, 256] => [b,128] => [b,10]
        h1 = tf.nn.relu(tf.matmul(x_, w1) + b1)
        h2 = tf.nn.relu(tf.matmul(h1, w2) + b2)
        out = tf.matmul(h2, w3) + b3

        # [b, 10]
        prob = tf.nn.softmax(out, axis=1) # tf.float32
        # [b, 1]
        pred = tf.argmax(prob, axis=1) # 索引号(类别)
        pred = tf.cast(pred, dtype=tf.int32)
        # y:[b]
        correct = tf.cast(tf.equal(pred, y_), dtype=tf.int32)
        correct = tf.reduce_sum(correct)

        total_correct += int(correct)
        total_sum += int(tf.cast(x_.shape[0], tf.int32))
    acc = total_correct / total_sum
    print(f'evaluation: acc={acc}')