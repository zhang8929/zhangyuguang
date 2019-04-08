#!/usr/bin/env python
# coding: utf-8


import sys, os, time
import gensim
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

train_path = "%s/%s" % ('/Users/zhangyuguang/Documents/data/', '0404_faq.txt')
# model_dir  = os.path.dirname(os.path.realpath(__file__)) +\
#                         '/Users/zhangyuguang/Documents/model/';
model_dir = '/Users/zhangyuguang/Documents/model/'

docs = {}
with open(train_path) as fh :
    index = 0
    for line in fh :
        l = line.strip()
        docs[index] = l
        index += 1
    fh.close()



#model_name = "100w_300d_w15_m1_e20.bin"
#model_name = "100w_300d_w15_m1_e40.bin"
#model_name = "100w_250d_w15_m1_e50.bin"
#model_name = "100w_250d_w15_m1_e2.bin"
#model_name = "100w_150d_w15_m1_e100.bin"
#model_name = "100w_150d_w15_m1_e200.bin"
#model_name = "100w_100d_w15_m1_e200.bin"
model_name = "100w_100d_w15_m1_e400.bin"
model_path = "%s/%s" % (model_dir, model_name)
model_dm = gensim.models.Doc2Vec.load(model_path)

def test():
    #text = '流鼻血 止不住 怎么办'
    #text = '盆腔炎 怎么 治疗'
    text = '睡觉 手麻 是 什么 问题'
    words = text.split()
    #test_text = '早上起来恶心是怎么回事'
    #获得对应的输入句子的向量
    inferred_vector_dm = model_dm.infer_vector(doc_words=words)
    #inferred_vector_dm = model_dm.infer_vector(doc_words=words, alpha=0.025, steps=500)
    #返回相似的句子
    t0 = time.time()
    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)
    t1 = time.time()
    print "ORIG: %s\n--------" % ''.join(words)
    for (i, sim) in sims :
        print "%d, %.04f, %s" % (i, sim, docs[i])
    print "USED TIME: %.03f" % (t1 - t0)


test()
