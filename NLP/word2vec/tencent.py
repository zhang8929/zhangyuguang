#!/usr/bin/env python
# coding: utf-8


import sys, os
# import modules & set up logging
import gensim, logging
import time
from gensim.models import KeyedVectors

class TencentVector(object) :

    __model = None

    def __init__ (self ) :
        pass

    def build_binary_vector(self, model_txt_path, model_bin_path) :
        self.__model = KeyedVectors.load_word2vec_format(model_txt_path, binary=False)
        self.__model.save_word2vec_format(model_bin_path, binary=True)

    def load_binary_vector (self, model_bin_path) :
        self.__model = gensim.models.Word2Vec.load(model_bin_path)

        print "语料数：%d" % self.__model.corpus_count
        print "词表长度：%d" % len(self.__model.wv.vocab)

if __name__ == '__main__' :

    txt_path = './xxx.txt'
    bin_path = './xxx.bin'

    v = TencentVector()

    # 把txt格式的腾讯向量文件，转成binary格式的
    v.build_binary_vector(txt_path, bin_path)

    # 加载binary格式的向量文件，只要不报错，就OK
    #v.load_binary_vector(bin_path)


'''
keyword = '咳嗽'
print "%s的相似度：\n" % (keyword)
words = ('睡不着', '睡醒', '喝水', '犯困')
for w in words :
    x = model.similarity(keyword, w)
    print "%s和<%s>的相似度是:%s" % (keyword, w, x)

def find_similar_words (keyword, TopN = 10) :
    t1 = time.time()
    n = TopN
    rs = model.wv.most_similar([keyword], topn=n)
    t2 = time.time()
    print "\n%s的TOP%s 强关系词分别是(用时%.02fs):\n---------------\n" %\
         (keyword, n, (t2 - t1))
    for (a, b) in rs :
        print "%s\t%s" %( a, b)

keywords = ('咳嗽', '胸闷', '吐痰', '失眠')
for word in keywords :
    find_similar_words (word)

'''

