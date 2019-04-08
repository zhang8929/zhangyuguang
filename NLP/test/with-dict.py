#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sys, os
import random
sys.path.insert(0, '..')

from keras.preprocessing.text import one_hot
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from semantics.cws import ChineseWordSplit

class SentenceLoader(object):

    def __init__ (self, words_file_path) :

        sentence_list = []
        with open(words_file_path) as fh :
            for line in fh :
                line = line.strip()
                result = int(line[-1])
                sentence = line[:-1]
                sentence_list.append((sentence, result))
            fh.close()

        random.shuffle (sentence_list)

        self.__training_list = sentence_list[:-18]
        self.__predict_list  = sentence_list[-18:]

    def get_sentence (self, type='training') :

        lists = []

        if type == 'training' :
            for (s, r) in self.__training_list :
                lists.append(s)
        else :
            for (s, r) in self.__predict_list :
                lists.append(s)

        return lists

    def get_result (self, type='training') :

        lists = []

        if type == 'training' :
            for (s, r) in self.__training_list :
                lists.append(r)
        else :
            for (s, r) in self.__predict_list :
                lists.append(r)

        return lists



class TextTrain(object) :

    __docs = None
    __orig_docs = None
    __labels = None
    __docs_max_length = None
    __vocab_size = None
    __enc_docs = None
    __pad_docs = None
    __cws = None
    __embedding_output_dim = 300
    __embedding_matrix = None

    def __init__(self, docs, labels) :

        self.__orig_docs = docs
        self.__cws = ChineseWordSplit()
        docs2 = self.__split_chinese_words(docs)

        self.__docs = docs2
        self.__labels = labels
        self.__tokenizer = Tokenizer()
        self.__tokenizer.fit_on_texts(self.__docs)
        self.__get_vocab_size()
        self.__build_embedding_matrix()

    def __split_chinese_words(self, docs) :

        sentence_list = []
        for doc in docs :
            ts = self.__cws.text_to_sequence(doc)
            sentence_list.append(' '.join(ts))

        return sentence_list

    # 载入训练好的词向量
    def __build_embedding_matrix (self) :

        #dict_path = '../' + 'database/ignore/medicine_words_300d.txt'
        dict_path = '../' + 'database/ignore/medicine_words_35w_300d.txt'
        #dict_path = '../' + 'database/ignore/Zhihu_QA/sgns.zhihu.word'
        #dict_path = '../' + 'database/ignore/Zhihu_QA/sgns.zhihu.bigram'
        words_index = dict()
        with open(dict_path, 'r')  as fh:
            fh.readline()
            for line in fh :
                words = line.split()
                word = words[0]
                cefs = np.asarray(words[1:], dtype='float32')
                words_index[word] = cefs
            fh.close()

        matrix = np.zeros((self.__get_vocab_size(), self.__embedding_output_dim))
        for word, index in self.__tokenizer.word_index.items() :
            embedding_vector = words_index.get(word.encode('utf8'))
            if embedding_vector is not None :
                matrix[index] = embedding_vector

        self.__embedding_matrix = matrix

    def __get_vocab_size (self) :

        self.__vocab_size = len(self.__tokenizer.word_index) + 1
        return self.__vocab_size

    def __get_docs_max_length (self) :
        max_length = 0
        for doc in self.__enc_docs :
            llen = len(doc)
            if llen > max_length :
                max_length = llen

        self.__docs_max_length = max_length
        return self.__docs_max_length

    def __build_one_hot_docs (self) :

        enc_docs = []

        for doc in self.__docs :
            x = one_hot(doc, self.__get_vocab_size())
            enc_docs.append(x)

        self.__enc_docs = enc_docs

    def __build_padded_docs (self) :
        self.__pad_docs = pad_sequences(self.__enc_docs,\
                             maxlen=self.__get_docs_max_length(), padding='post')

        #seqs = tokenizer.texts_to_sequences(self.__docs)
        #print seqs

    def build_model(self) :

        self.__build_one_hot_docs()
        self.__build_padded_docs()

        print self.__pad_docs

        e = Embedding(self.__vocab_size, \
            self.__embedding_output_dim, weights=[self.__embedding_matrix],\
            input_length=self.__docs_max_length,\
            trainable=False)

        #e = Embedding(self.__vocab_size, self.__embedding_output_dim,\
        #    input_length=self.__docs_max_length)



        self.model = Sequential()
        self.model.add(e)
        self.model.add(Flatten())
        self.model.add(Dense(1, activation='sigmoid'))

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        #self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

        print self.model.summary()

    # 训练
    def train(self, epochs=50) :
        self.model.fit(self.__pad_docs, self.__labels, epochs=epochs, verbose=1)

    # 评估
    def evalute(self) :
        loss, accuracy = self.model.evaluate(self.__pad_docs, self.__labels, \
                verbose=1)
        print "准确度: %f, 损失度: %f" % (accuracy*100, loss*100)

    def predict(self, text) :

        ts = self.__cws.text_to_sequence(text)
        t0 = ' '.join(ts)

        t1 = one_hot(t0, self.__vocab_size)
        t2 = [t1]

        t3 = pad_sequences(t2, maxlen=self.__docs_max_length, padding='post')

        out = self.model.predict(t3)
        result = out[0][0]
        return result


if __name__ == '__main__' :


    medicine_sentence = os.path.dirname(os.path.realpath(__file__))  +\
        '/../database/QingGan/medicine_words_100.txt'

    docs = SentenceLoader(medicine_sentence)
    cn_docs = docs.get_sentence('training')
    labels  = docs.get_result('training')

    test= TextTrain(cn_docs, labels)
    test.build_model()
    test.train(1000)
    test.evalute()

    predict_sentence = docs.get_sentence('predict')
    predict_result   = docs.get_result ('predict')

    index = 0
    for sentence in predict_sentence :

        r1 = test.predict(sentence)
        r0 = predict_result[index]
        print "PREDICT: %.04f, ORIG: %d, %s" % (r1, r0, sentence)

        index += 1
