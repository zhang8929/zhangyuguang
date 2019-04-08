#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sys
sys.path.insert(0, '..')

from keras.preprocessing.text import one_hot
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from semantics.cws import ChineseWordSplit

class TextTrain(object) :

    __docs = None
    __orig_docs = None
    __labels = None
    __docs_max_length = None
    __vocab_size = None
    __enc_docs = None
    __pad_docs = None
    __cws = None
    __embedding_output_dim = 32

    def __init__(self, docs, labels) :

        self.__orig_docs = docs
        self.__cws = ChineseWordSplit()
        docs2 = self.__split_chinese_words(docs)

        self.__docs = docs2
        self.__labels = labels
        self.__tokenizer = Tokenizer()
        self.__tokenizer.fit_on_texts(self.__docs)

    def __split_chinese_words(self, docs) :

        sentence_list = []
        for doc in docs :
            ts = self.__cws.text_to_sequence(doc)
            sentence_list.append(' '.join(ts))

        return sentence_list

    def __get_vocab_size (self) :

        self.__vocab_size = len(self.__tokenizer.word_index)
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

        e = Embedding(self.__vocab_size, self.__embedding_output_dim,\
            input_length=self.__docs_max_length)

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
        print text, t0
        t1 = one_hot(t0, self.__vocab_size)
        t2 = [t1]
        print t2

        t3 = pad_sequences(t2, maxlen=self.__docs_max_length, padding='post')
        print t3

        out = self.model.predict(t3)
        print out


# 测试文档
'''
docs = ['Well done!',
		'Good work',
		'Great effort',
		'nice work',
		'Excellent!',
		'Weak',
		'Poor effort!',
		'not good',
		'poor work',
		'Could have done better.']
'''

cn_docs = ['做的不错',
        '工作出色',
        '很好的效果',
        '值得学习',
        '效果很赞',
        '做的很差',
        '工作拖延',
        '效果很差',
        '工作要批评',
        '很糟糕的效果']

# 文档的分类标签
labels = [1,1,1,1,1,0,0,0,0,0]


if __name__ == '__main__' :

    test= TextTrain(cn_docs, labels)
    test.build_model()
    test.train(1000)
    test.evalute()
    test.predict('工作很糟糕')
    test.predict('不错的效果')
    test.predict('做的很差')
    test.predict('效果不错')
    test.predict('进度不错')
