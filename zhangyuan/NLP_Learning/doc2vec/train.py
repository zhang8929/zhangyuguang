#!/usr/bin/env python
# coding: utf-8


import sys, os
import gensim
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


train_dir  = os.path.dirname(os.path.realpath(__file__)) +\
                        '';
train_path = "%s/%s" % (train_dir, 'doc_yuliao.txt')
model_dir  = os.path.dirname(os.path.realpath(__file__)) +\
                        '';
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
         min_count=min_counts)

    #model.train(docs, total_examples=model.corpus_count, epochs=30)

    model_name = "100w_%sd_w%s_m%s_e%s.bin" % (vector_size, window,\
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