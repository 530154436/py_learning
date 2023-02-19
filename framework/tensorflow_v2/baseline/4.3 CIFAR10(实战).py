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
    x = tf.reshape(x, [32*32*3]) # (32, 32, 3) => (32*32*3)
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(tf.squeeze(y), depth=10) # 压缩维度1, [1,10] => [10]
    return x,y

# [50k,32,32,3], [50k,1]
# [10k,32,32,3], [10k,1]
(x,y), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
print_info(x, name='x_train')
print_info(y, name='y_train')
print_info(x_test, name='x_test')
print_info(y_test, name='y_test')

# 转换为Tensor、预处理、混洗、批次
train_db = tf.data.Dataset.from_tensor_slices(tensors=(x,y))
train_db = train_db.map(preprocess)\
                   .shuffle(10000)\
                   .batch(128)
test_db = tf.data.Dataset.from_tensor_slices(tensors=(x_test, y_test))
test_db = test_db.map(preprocess).batch(128)

# 打印样例, batch: (128, 32*32*3) (128, 10)
sample = next(iter(train_db))
print(f'batch: sample[0].shape={sample[0].shape}, sample[1].shape={sample[1].shape}')

# 模型定义
class MyDenseLayer(layers.Layer):

    def __init__(self, input_dim, output_dim, activation):
        super(MyDenseLayer, self).__init__()
        self.activation = activation
        self.kernel = self.add_variable(name='w', shape=[input_dim, output_dim])
        # self.bias = self.add_variable(name='b', shape=[output_dim])

    def call(self, inputs, training=None):
        '''
        计算逻辑
        :param inputs: [b,32*32*3]
        '''
        output = tf.matmul(inputs, self.kernel)
        if self.activation:
            output = self.activation(output)
        return output

class MyModel(models.Model):

    def __init__(self):
        super(MyModel, self).__init__()
        self.full_layer_1 = MyDenseLayer(32*32*3,256, activation=tf.nn.relu)
        self.full_layer_2 = MyDenseLayer(256, 128, activation=tf.nn.relu)
        self.full_layer_3 = MyDenseLayer(128, 64, activation=tf.nn.relu)
        self.full_layer_4 = MyDenseLayer(64, 32, activation=tf.nn.relu)
        self.full_layer_5 = MyDenseLayer(32, 10, activation=tf.nn.relu)

    def call(self, inputs, training=None, mask=None):
        '''
        计算逻辑
        :param inputs: [b,32*32*3]
        '''
        x = self.full_layer_1(inputs)
        x = self.full_layer_2(x)
        x = self.full_layer_3(x)
        x = self.full_layer_4(x)
        x = self.full_layer_5(x)
        return x

def create_model():
    '''
    创建模型
    '''
    model = MyModel()
    model.compile(optimizer=optimizers.Adam(lr=1e-3),
                  loss=tf.compat.v2.keras.losses.CategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    return model

model = create_model()
model.fit(train_db, validation_data=test_db, epochs=5)
model.evaluate(test_db)
model.save_weights('models/cifar10/weights.ckpt')
del model
model = create_model()
model.load_weights('models/cifar10/weights.ckpt')
model.evaluate(test_db)











