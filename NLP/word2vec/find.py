#!/usr/bin/env python
# coding: utf-8


import sys, os
# import modules & set up logging
import gensim, logging
import time
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



model_dir  = os.path.dirname(os.path.realpath(__file__)) + '/../models';
model_path = "%s/%s" % (model_dir, '2018121301.bin')

model = gensim.models.Word2Vec.load(model_path)

print "语料数：%d" % model.corpus_count
print "词表长度：%d" % len(model.wv.vocab)

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


