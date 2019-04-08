#!/usr/bin/env python
# coding: utf-8


import sys, os
import gensim
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import time
print time.ctime()
# train_dir  = os.path.dirname(os.path.realpath(__file__)) +\
#                         '/Users/zhangyuguang/Documents/data/';
train_path = "%s/%s" % ('/Users/zhangyuguang/Documents/data/', '0404_user.txt')
# model_dir  = os.path.dirname(os.path.realpath(__file__)) +\
#                         '/Users/zhangyuguang/Documents/model/';
model_dir = '/Users/zhangyuguang/Documents/model/'
#sentences  = MySentences(train_dir) # a memory-friendly iterator

TaggededDocument = gensim.models.doc2vec.TaggedDocument

def get_train_data (max_lines = None) :

    docs = []
    with open(train_path) as fh :
        index = 0
        for line in fh :
            l = line.strip()
            words = l.split()
            docs.append(TaggededDocument(words, tags=[index]))
            index += 1
            if max_lines > 0 and index>=max_lines :
                break
        fh.close()

    return docs

# 训练，忽略词频小于3的词语
#model = gensim.models.Doc2Vec(docs, min_count=9, window=3, vector_size=100, sample=1e-3, negative=5, workers=4)


def build_model (docs, vector_size, window, min_counts, epochs) :

    model = gensim.models.Doc2Vec(docs,\
        workers=4, \
        vector_size=vector_size,\
        window=window,\
        # dm = 1 dm-pv  0  dbow
        dm=1,\
        epochs=epochs,\
        sample=1e-5,\
        negative=5,\
        alpha=0.025,
        min_alpha=0.025,\
         min_count=min_counts
        )
    print time.ctime()

    #model.train(docs, total_examples=model.corpus_count, epochs=30)

    model_name = "0404_user_w_%sd_w%s_m%s_e%s.bin" % (vector_size, window,\
                 min_counts, epochs)
    model_path = "%s/%s" % (model_dir, model_name)
    model.save(model_path)

docs = get_train_data(None)
#build_model(docs, 300, 15, 1, 20)
#build_model(docs, 300, 15, 1, 40)
#build_model(docs, 200, 15, 1, 30)
#build_model(docs, 250, 15, 1, 50)
#build_model(docs, 150, 15, 1, 100)
#build_model(docs, 150, 15, 1, 200)
#build_model(docs, 100, 15, 1, 200)
build_model(docs, 100, 15, 1, 400)
'''参数说明'''
#min_count: 可以对字典做截断. 词频少于min_count次数的单词会被丢弃掉, 默认值为5。

#alpha: 是初始的学习速率，在训练过程中会线性地递减到min_alpha。

#window：窗口大小，表示当前词与预测词在一个句子中的最大距离是多少。

#·size：是指特征向量的维度，默认为100。大的size需要更多的训练数据,但是效果会更好. 推荐值为几十到几百。

#Dm：训练算法：默认为1，指DM；dm=0,则使用DBOW。

#workers：用于控制训练的并行数。

#iter：语料库上的迭代次数。他默认继承Word2vec是5，但值10或20是常见的Paragraph Vector。
