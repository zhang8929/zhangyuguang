#!/usr/bin/env python
# coding: utf-8

'''
基于keras 实现

利用之前训练好的词向量，基于keras使用1D卷积神经网络完成文本分类任务。

总结

训练集准确率92.29%左右，测试集准确率74.96%左右，说明模型可能过拟合了。没关系，我们已经实现了目标。整个流程跑通了。为了提高准确率，可以尝试：
1、增加文章数量，这次测试我用的文章不多
2、文章类别均衡些，这次我用的文章类别严重有偏，某些类别文章特别多
3、尝试dropout和Batch normalization控制过拟合
4、尝试改变网络结构

'''


from __future__ import print_function
import os
import sys
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
import gensim
import pandas as pd

MAX_SEQUENCE_LENGTH = 1000 # 每篇文章选取1000个词
MAX_NB_WORDS = 10000 # 将字典设置为含有1万个词
EMBEDDING_DIM = 300 # 词向量维度，300维
VALIDATION_SPLIT = 0.2 # 测试集大小，全部数据的20%


# 目的是得到一份字典(embeddings_index)含有1万个词，每个词对应属于自己的300维向量
embeddings_index = {}

print('Indexing word vectors.')
path = '../word2vec_model'
model = gensim.models.Word2Vec.load(path)
word_vectors = model.wv
for word, vocab_obj in model.wv.vocab.items():
    if int(vocab_obj.index) < MAX_NB_WORDS:
        embeddings_index[word] = word_vectors[word]
del model, word_vectors # 删掉gensim模型释放内存
print('Found %s word vectors.' % len(embeddings_index))

# print out:
# Indexing word vectors.
# Found 10000 word vectors.


print('Processing text dataset')

texts = []  # list of text samples
labels = []  # list of label ids
labels_index = {}  # label与name的对应关系

# 读取数据
path = '../content.csv'
contents = pd.read_csv(path)
contents = contents.dropna()

# 提取文本内容与label
texts = contents['content'].values.tolist()
labels = contents['channel_id'].map(int)
labels = labels.values.tolist()

# 获得label与name的对应关系
tem_labels_index = contents.groupby(['name', 'channel_id']).size().reset_index()
tem_labels_index = tem_labels_index[['channel_id', 'name']].values.tolist()
for idx, name in tem_labels_index:
    labels_index[name] = idx
del contents, tem_labels_index

print('Found %s texts.' % len(texts))

# print out
# Processing text dataset
# Found 57867 texts.

tokenizer = Tokenizer(num_words=MAX_NB_WORDS) # 传入我们词向量的字典
tokenizer.fit_on_texts(texts) # 传入我们的训练数据，得到训练数据中出现的词的字典
sequences = tokenizer.texts_to_sequences(texts) # 根据训练数据中出现的词的字典，将训练数据转换为sequences

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH) # 限制每篇文章的长度

labels = to_categorical(np.asarray(labels)) # label one hot表示
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

# print out
# Found 379653 unique tokens.
# Shape of data tensor: (57867, 1000)
# Shape of label tensor: (57867, 26) # 我的文本类别有26类

# 打乱文章顺序
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])

# 切割数据
x_train = data[:-num_validation_samples]
y_train = labels[:-num_validation_samples]
x_val = data[-num_validation_samples:]
y_val = labels[-num_validation_samples:]

num_words = min(MAX_NB_WORDS, len(word_index))  # 对比词向量字典中包含词的个数与文本数据所有词的个数，取小
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NB_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # 文本数据中的词在词向量字典中没有，向量为取0；如果有则取词向量中该词的向量
        embedding_matrix[i] = embedding_vector

# 将预训练好的词向量加载如embedding layer
# 我们设置 trainable = False，代表词向量不作为参数进行更新
embedding_layer = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)

# 训练  1D 卷积神经网络 使用 Maxpooling1D
sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)
x = Conv1D(filters=128, kernel_size=5, activation='relu')(embedded_sequences)
x = MaxPooling1D((pool_size=5)(x)
x = Conv1D(filters=128, kernel_size=5, activation='relu')(x)
x = MaxPooling1D((pool_size=5)(x)
x = Conv1D(filters=128, kernel_size=5,, activation='relu')(x)
x = MaxPooling1D((pool_size=35)(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
preds = Dense(len(labels_index), activation='softmax')(x)

model = Model(sequence_input, preds)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['acc'])

# 如果希望短一些时间可以，epochs调小
model.fit(x_train, y_train,
          batch_size=128,
          epochs=50,
          validation_data=(x_val, y_val))


