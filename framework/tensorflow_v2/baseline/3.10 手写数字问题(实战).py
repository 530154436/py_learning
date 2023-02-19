# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import numpy as np
import tensorflow as tf
from tensorflow.python.keras import layers,Sequential,metrics

tf.compat.v1.enable_eager_execution()  # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

def print_info(x, name=''):
    '''
    打印信息
    '''
    if isinstance(x, np.ndarray):
        print(f'ndarray: {name}.shape={x.shape}, type({name})={type(x)}, min({name})={x.min()}, max({name})={x.max()}')
    elif isinstance(x, tf.Tensor):
        print(f'Tensor: {name}.shape={x.shape}, {name}.dtype={x.dtype}')

def load_data_set(batch_size):
    '''
    加载数据集
    :return: x,y,x_test,y_test
    '''
    def preprocess(x, y, x_name='x', y_name='y'):
        '''
        预处理
        '''
        x = tf.cast(x, dtype=tf.float32) / 256
        y = tf.cast(y, dtype=tf.int32)

        print_info(x, name=x_name)
        print_info(y, name=y_name)

        return x,y

    # (60000, 28, 28), (60000,), (10000, 28, 28), (10000,)
    (x,y), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    print_info(x, name='x_train')
    print_info(y, name='y_train')
    print_info(x_test, name='x_test')
    print_info(y_test, name='y_test')

    # 预处理、混洗、设置批次
    train_db = tf.data.Dataset.from_tensor_slices((x,y))
    train_db = train_db.map(lambda x,y:preprocess(x,y, x_name='x_test', y_name='y_test'))\
                       .shuffle(10000)\
                       .batch(batch_size=batch_size)

    # 样例
    train_db_iter = iter(train_db)
    sample = next(train_db_iter)
    print(f'Train Sample: x(batch)={sample[0].shape}, y(batch)={sample[1].shape}\n')

    db_test = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    db_test = db_test.map(lambda x,y:preprocess(x,y, x_name='x_test', y_name='y_test'))\
                     .shuffle(10000)\
                     .batch(batch_size=batch_size)

    return train_db,db_test

def model_fn(input_shape):
    '''
    构造模型
    '''
    # 容器
    model = Sequential( name='手写数字问题(线性层)',
                        layers=[layers.Dense(units=256, activation=tf.nn.relu), # [b,784] => [b,256]
                               layers.Dense(units=128, activation=tf.nn.relu), # [b,256] => [b,128]
                               layers.Dense(units=64, activation=tf.nn.relu),  # [b,128] => [b,64]
                               layers.Dense(units=32, activation=tf.nn.relu),  # [b,64]  => [b,32]
                               layers.Dense(units=10, activation=tf.nn.relu)]) # [b,32]  => [b,10]
    model.build(input_shape=input_shape)
    print(model.summary())
    return model

def main(epochs=30, batch_size=128):

    db_train, db_test = load_data_set(batch_size)
    model = model_fn(input_shape=(None, 28*28))
    optimizer = tf.keras.optimizers.Adam(lr=1e-3)

    # metrics-Step1. Build a meter
    acc_meter = metrics.Accuracy()
    loss_meter = metrics.Mean()

    for epoch in range(epochs):
        for step,(x,y) in enumerate(db_train):

            # [b,28,28] => [b,784]
            x = tf.reshape(x, (-1, 28*28))

            with tf.GradientTape() as tape:

                # [b,784] => [b,10]
                logits = model(x)
                y = tf.one_hot(y, depth=10)

                # [b]
                # loss = tf.reduce_mean(tf.compat.v2.losses.MSE(y_true=y, y_pred=logits))
                loss = tf.reduce_mean(tf.compat.v2.losses.categorical_crossentropy(y_true=y,
                                                                                   y_pred=logits,
                                                                                   from_logits=True))
            grads = tape.gradient(target=loss, sources=model.trainable_variables) # len(trainable_variables) = 10
            optimizer.apply_gradients(grads_and_vars=zip(grads,model.trainable_variables))

            if step%100 == 0:
                print(f'epoch,step,loss: {epoch}, {step}, {float(loss)}')

                loss_meter.reset_states() # 更新loss

        total_correct, total = 0, 0

        # metrics-Step2. clear buffer
        acc_meter.reset_states()

        # tes/evaluation
        for step, (x_, y_) in enumerate(db_test):
            # [b, 28, 28] => [b, 28*28]
            x_ = tf.reshape(x_, [-1, 28 * 28])  # [128,784]

            # [b,10]
            logits = model(x_)

            # logits => prob,[b,10]
            prob = tf.nn.softmax(logits, axis=-1)
            pred = tf.cast(tf.argmax(prob, axis=-1), dtype=tf.int32)

            # y:[b], correct:[b]
            correct = tf.equal(y_, pred)
            total_correct += tf.reduce_sum(tf.cast(correct, dtype=tf.int32))

            total += x_.shape[0]

            # metrics-Step3. Update Data
            acc_meter.update_state(y_, pred)

        # metrics-Step4. Get Average Data
        print(epoch, 'Evaluate Acc:', total_correct / total, acc_meter.result().numpy())

if __name__ == '__main__':
    main()