#!/usr/bin/env python
# coding: utf-8


import sys, os
# import modules & set up logging
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


train_dir  = os.path.dirname(os.path.realpath(__file__)) + '/../train';
train_path = "%s/%s" % (train_dir, '2018121301.txt')
model_dir  = os.path.dirname(os.path.realpath(__file__)) + '/../models';
model_path = "%s/%s" % (model_dir, '2018121301.bin')
sentences  = MySentences(train_dir) # a memory-friendly iterator

# 训练，忽略词频小于3的词语
model = gensim.models.Word2Vec(sentences, workers=3, \
        size=300, window=6, min_count=2)

model.save(model_path)


