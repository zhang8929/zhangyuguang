#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import gensim
import sklearn
import numpy as np

from gensim.models.doc2vec import Doc2Vec, LabeledSentence

TaggededDocument = gensim.models.doc2vec.TaggedDocument


def get_datasest():
    with open("/home/python/Desktop/nlp/fenci.txt", 'r') as cf:
        docs = cf.readlines()
        print (len(docs))

    x_train = []
    # y = np.concatenate(np.ones(len(docs)))
    for i, text in enumerate(docs):
        word_list = text.split(' ')
        l = len(word_list)
        word_list[l - 1] = word_list[l - 1].strip()
        document = TaggededDocument(word_list, tags=[i])
        x_train.append(document)

    return x_train


def getVecs(model, corpus, size):
    vecs = [np.array(model.docvecs[z.tags[0]].reshape(1, size)) for z in corpus]
    return np.concatenate(vecs)


def train(x_train, size=200, epoch_num=1):
    model_dm = Doc2Vec(x_train, min_count=9, window=3, size=size, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=70)
    model_dm.save('/home/python/Desktop/nlp/model_fenci')

    return model_dm


def test():
    model_dm = Doc2Vec.load("/home/python/Desktop/nlp/model_fenci")
    test_text = ['晚上','胃疼','怎么办']
    inferred_vector_dm = model_dm.infer_vector(test_text)
    print (inferred_vector_dm)
    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)

    return sims


if __name__ == '__main__':
    x_train = get_datasest()
    model_dm = train(x_train)

    sims = test()
    for count, sim in sims:
        sentence = x_train[count]
        words = ''
        for word in sentence[0]:
            words1 = json.dumps(words, ensure_ascii=False, encoding='UTF-8')

            print(words1 + str(sim))
