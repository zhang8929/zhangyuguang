#!/usr/bin/env python
# coding: utf-8

import sys, time
import numpy as np
#from matplotlib import pyplot as plt

from keras.models import Sequential

# Keras的核心层
from keras.layers import Dense, Dropout, Activation, Flatten

# Keras的CNN 层
from keras.layers import Conv2D, MaxPooling2D

# Keras的优化器
from keras.optimizers import RMSprop

# Keras的实体工具
from keras.utils import np_utils

np.random.seed(123)


# 从MNIST中加载图像数据
from keras.datasets import mnist

# 将MNIST 数据加载为训练集和测试集
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()





# 为Keras预处理数据

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

Y_train = np_utils.to_categorical(Y_train, 10)
Y_test = np_utils.to_categorical(Y_test, 10)


'''
定义模型架构

开始构建模型，模型分包含两个隐层和一个输出层,都是全连接层，使用Sequential构建

其中隐层输出采用ReLU激活函数，Sequential的第一层要指定input_shape，要注意，这里的input_shape 是不包含batch大小的，就只是后面几维

'''

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))

# 输出网络结构
model.summary()

'''
配置模型，主要包括

loss：     loss计算方法（损失函数)
optimizer：优化函数
metrics：  指定哪些量需要在训练及测试中关注，一般都会写accuracy
'''
model.compile(\
    loss='categorical_crossentropy',\
    optimizer=RMSprop(),\
    metrics=['accuracy']\
    )

#print model.output_shape

'''
开始训练。这里使用的是model对象的fit方法。前两个参数分别是完整的训练数据和训练标签

batch_size 表示每一次塞入多少张图片
epochs     表示训练几轮

verbose    表示用何种方式显示输出信息，
           0表示不输出，1表示在一直输出更新，2表示每一个epoch才输出一次

validation_data
           表示验证集，格式和训练集一样，
           如果此参数不为空的话，每一个epoch过后就会输出验证集的loss和accuracy
'''

model.fit(X_train, Y_train, \
        batch_size=64, \
        epochs=2, \
        verbose=1, \
        validation_data=(X_test, Y_test)\
       )

'''
测试结果，输出为loss以及其他之前compile模型时指定过的metrics的值

'''


score = model.evaluate(X_test, Y_test, verbose=1)
print 'Test loss:', score[0]
print 'Test accuracy', score[1]
