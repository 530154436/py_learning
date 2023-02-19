# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import tensorflow as tf
from pathlib import Path
from tensorflow.python.keras import layers,optimizers,metrics,Sequential

tf.compat.v1.enable_eager_execution()   # 开启 Eager 模式
os.environ["TF_CPP_MIN_LOG_LEVEL"]='10' # 只显示 warning 和 Error

# Keras高层API: datasets、layers、losses、metrics、optimizers

'''
    1. 预处理、准备数据(Dataset)
'''
def preprocess(x, y):
    """
    x is a simple image, not a batch
    """
    x = tf.cast(x, dtype=tf.float32) / 255.
    x = tf.reshape(x, [28*28])
    y = tf.cast(y, dtype=tf.int32)
    y = tf.one_hot(y, depth=10)
    return x,y

# 加载数据 [60k,28,28]
batchsz = 128
(x, y), (x_val, y_val) = tf.compat.v2.keras.datasets.mnist.load_data()
print('datasets:', x.shape, y.shape, x.min(), x.max())

# 预处理
train_x_y = tf.data.Dataset.from_tensor_slices((x, y))              # 训练集
train_x_y = train_x_y.map(preprocess).shuffle(60000).batch(batchsz)
val_x_y = tf.data.Dataset.from_tensor_slices((x_val, y_val)) # 验证集
val_x_y = val_x_y.map(preprocess).batch(batchsz)

'''
    2. 自定义层/网络
       - model(x) <=> model.__call__(x)
       - 继承 tf.keras.layers.Layer、keras.Model
         - __init__、call(逻辑)
'''
class MyDenseLayer(layers.Layer):

    def __init__(self, input_dim, output_dim, activation=None):
        super(MyDenseLayer, self).__init__()
        self.activation = activation

        # Layer.add_weight
        self.kernel = self.add_variable(name='w', shape=[input_dim, output_dim])
        self.bias = self.add_variable(name='b', shape=[output_dim])

    def call(self, inputs, training=None):
        output = tf.matmul(inputs, self.kernel) + self.bias
        if self.activation:
            output = self.activation(output)
        return output

class MyModel(tf.compat.v2.keras.Model):

    def __init__(self):
        super(MyModel, self).__init__()
        self.full_layer_1 = MyDenseLayer(28*28,256, activation=tf.nn.relu)
        self.full_layer_2 = MyDenseLayer(256, 128, activation=tf.nn.relu)
        self.full_layer_3 = MyDenseLayer(128, 64, activation=tf.nn.relu)
        self.full_layer_4 = MyDenseLayer(64, 32, activation=tf.nn.relu)
        self.full_layer_5 = MyDenseLayer(32, 10, activation=tf.nn.relu)

    def call(self, inputs, training=None, mask=None):
        '''
        计算逻辑
        :param inputs:   [b,28*28]
        '''
        x = self.full_layer_1(inputs)
        x = self.full_layer_2(x)
        x = self.full_layer_3(x)
        x = self.full_layer_4(x)
        x = self.full_layer_5(x)
        return x

def create_model(use_custom=True):
    '''
    创建模型
    :param use_custom: 使用自定义模型
    '''
    model = None
    if use_custom:
        model = MyModel()
        model.compile(optimizer=optimizers.Adam(lr=1e-3),
                      loss=tf.compat.v2.keras.losses.CategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        return model
    else:
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
    return model

# 是否使用自定义模型
use_custom = False

'''
    3. compile、fit、evaluate、predict
'''
model = create_model(use_custom=use_custom)
model.fit(train_x_y,
          epochs=1,
          validation_data=val_x_y,
          validation_freq=2)
print(model.summary())

'''
    4. 模型保存与加载
      - save/load weights
      - save/load entire model
      - saved_model
'''
# (1) weights
model.save_weights('models/weights/weights.ckpt')   # 保存权重
del model                                           # 删除模型
model = create_model(use_custom=use_custom)         # 创建模型实例
model.load_weights('models/weights/weights.ckpt')   # 恢复权重

# (2) entire model
#  => 自定义模型该方法不适用 (use_custom=True)
#  => It does not work for subclassed models
# model.save('models/model.h5', include_optimizer=False) # 将整个模型保存为HDF5文件
# del model
# model = tf.compat.v2.keras.models.load_model('models/model.h5')
# model.compile(optimizer=optimizers.Adam(lr=1e-3),
#               loss=tf.compat.v2.keras.losses.CategoricalCrossentropy(from_logits=True),
#               metrics=['accuracy'])

# (3) saved_model (预测有问题)
# saved_model_path = 'models/saved_model'
# tf.compat.v1.keras.experimental.export_saved_model(model, saved_model_path)
# del model
# # 必须在评估之前编译模型。
# # 如果仅部署已保存的模型，则不需要此步骤。
# model = tf.compat.v1.keras.experimental.load_from_saved_model(saved_model_path)
# model.compile(optimizer=optimizers.Adam(lr=1e-3),
#               loss=tf.compat.v2.keras.losses.CategoricalCrossentropy(from_logits=True),
#               metrics=['accuracy'])

'''
    5. evaluate
'''
model.evaluate(val_x_y)

'''
    6. predict
'''
sample = next(iter(train_x_y))
x,y = sample[0],sample[1]
print(x.shape, y.shape)
pred = model.predict(x, steps=1)
print(y, pred)
# convert back to number
y = tf.argmax(y, axis=1)
pred = tf.argmax(pred, axis=1)
print(pred)
print(y)






