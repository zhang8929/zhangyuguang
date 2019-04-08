#!/usr/bin/env python
# coding: utf-8

## 文本分类

import numpy as np
import sys, os
import random
sys.path.insert(0, '..')

from keras.preprocessing.text import one_hot
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model, load_model
from keras.layers import Flatten
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.utils import to_categorical
from keras.layers.embeddings import Embedding
from semantics.cws import ChineseWordSplit

class IntentLoader (object) :

    __orig_intents = None
    __indexes_key  = None
    __keys_index   = None

    def __init__(self, train_file_path) :

        questions = []
        intents   = []

        with open(train_file_path, 'r') as fh :
            s = fh.read()
            lines = s.split("\n")
            index = 0
            for l in lines :
                index += 1
                line = l.strip()
                if len(line) == 0 :
                    continue

                if index % 2 == 1 :
                    questions.append(line)
                else :
                    intents.append(line)
            fh.close

        # 把字符串的intent转化成数字索引
        self.__orig_intents = intents
        intents = self.__build_intents(intents)

        ## debug
        #for i in range(len(intents)) :
        #    index = intents[i]
        #    print i, self.get_intent_word(index), self.__orig_intents[i]

        sentence_list = []
        for i in range(len(questions)) :
            sentence_list.append((questions[i], intents[i]))

        random.shuffle (sentence_list)
        predict_pos = -1 * int(0.1 * len(sentence_list))

        self.__training_list = sentence_list[:predict_pos]
        self.__predict_list  = sentence_list[predict_pos:]

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

        return to_categorical(lists)

    def get_intent_count(self) :
        return len(self.__indexes_key)

    def get_intent_word (self, index) :

        return self.__indexes_key[index]

    def __build_intents (self, intents) :

        keys_index = {}
        indexes_key = {}
        labels = []

        for word in intents :
           keys_index[word] = 1

        labels = keys_index.keys()
        for index in range(len(labels)):
            word = labels[index]
            keys_index[word] = index
            indexes_key[index] = word

        ints = []
        for intent in intents :
            index = keys_index.get(intent)
            ints.append(index)

        self.__keys_index = keys_index
        self.__indexes_key = indexes_key

        return ints


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
    __labels_dict_count = None

    def __init__(self, docs, labels, labels_dict_count) :

        self.__orig_docs = docs
        self.__cws = ChineseWordSplit()
        docs2 = self.__split_chinese_words(docs)

        self.__docs = docs2
        self.__labels = labels
        self.__labels_dict_count = labels_dict_count
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
        self.__docs_max_length = 150
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


    def __split_and_one_hot_and_padded_docs (self, docs) :


        enc_docs = []

        for doc in docs :
            ts = self.__cws.text_to_sequence(doc)
            t0 = ' '.join(ts)
            x = one_hot(t0, self.__get_vocab_size())
            enc_docs.append(x)

        pad_docs = pad_sequences(enc_docs,\
                             maxlen=self.__get_docs_max_length(), padding='post')

        return pad_docs

    def build_model(self) :

        self.__build_one_hot_docs()
        self.__build_padded_docs()

        #print self.__pad_docs

        '''
        e = Embedding(self.__vocab_size, \
            self.__embedding_output_dim, weights=[self.__embedding_matrix],\
            input_length=self.__docs_max_length,\
            trainable=False)

        self.model = Sequential()
        self.model.add(e)
        self.model.add(Flatten())
        self.model.add(Dense(1, activation='sigmoid'))

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        '''


        # load pre-trained word embeddings into an Embedding layer
        # note that we set trainable = False so as to keep the embeddings fixed
        # embedding_layer = Embedding(num_words,
        #                   EMBEDDING_DIM,
        #                   embeddings_initializer=Constant(embedding_matrix),
        #                   input_length=MAX_SEQUENCE_LENGTH,
        #                   trainable=False)
        embedding_layer = Embedding(self.__vocab_size, \
            self.__embedding_output_dim, weights=[self.__embedding_matrix],\
            input_length=self.__docs_max_length,\
            trainable=False)

        print('Training model.')

        # train a 1D convnet with global maxpooling
        print "docs_max_length: %d" % self.__docs_max_length
        sequence_input = Input(shape=(self.__docs_max_length,), dtype='int32')
        embedded_sequences = embedding_layer(sequence_input)
        x = Conv1D(128, 5, activation='relu')(embedded_sequences)
        x = MaxPooling1D(5)(x)
        x = Conv1D(128, 5, activation='relu')(x)
        x = MaxPooling1D(5)(x)
        x = Conv1D(128, 5, activation='relu')(x)
        x = GlobalMaxPooling1D()(x)
        x = Dense(128, activation='relu')(x)
        preds = Dense(self.__labels_dict_count, activation='softmax')(x)

        self.model = Model(sequence_input, preds)
        self.model.compile(loss='categorical_crossentropy',
                optimizer='rmsprop',
                metrics=['acc'])


        print self.model.summary()

    # 训练
    def train(self, epochs=50) :
        self.model.fit(self.__pad_docs, self.__labels, epochs=epochs, verbose=1)

    # 评估
    def evalute(self, docs, labels) :
        pDocs = self.__split_and_one_hot_and_padded_docs(docs)
        loss, accuracy = self.model.evaluate(pDocs, labels, verbose=1)
        print "准确度: %f, 损失度: %f" % (accuracy*100, loss*100)

    def save (self, model_path) :
        self.model.save(model_path)

    def load_model(self, path) :

        self.model = load_model(path)

    def predict(self, text) :

        ts = self.__cws.text_to_sequence(text)
        t0 = ' '.join(ts)

        t1 = one_hot(t0, self.__vocab_size)
        t2 = [t1]

        t3 = pad_sequences(t2, maxlen=self.__docs_max_length, padding='post')

        print t3
        out = self.model.predict(t3)
        print out
        return out


if __name__ == '__main__' :

    intent_file_path = os.path.dirname(os.path.realpath(__file__))  +\
            '/../database/Intent/training.txt'
    intent_model_path = os.path.dirname(os.path.realpath(__file__))  +\
            '/../database/Intent/model.h5'

    docs = IntentLoader(intent_file_path)
    cn_docs = docs.get_sentence('training')
    labels  = docs.get_result('training')
    predict_sentence = docs.get_sentence('predict')
    predict_result   = docs.get_result ('predict')
    labels_dict_count = docs.get_intent_count()


    if len(sys.argv) >= 2 and sys.argv[1] == 'train' :
    # 训练和保存模型

        test= TextTrain(cn_docs, labels, labels_dict_count)
        test.build_model()
        test.train(25)
        test.evalute(predict_sentence, predict_result)

        for sentence in predict_sentence :
            result = test.predict(sentence)

        test.save(intent_model_path)
    else :
    # 载入模型

        test= TextTrain(cn_docs, labels, labels_dict_count)
        test.load_model(intent_model_path)
        for sentence in predict_sentence :
            result = test.predict(sentence)

    #index = 0
    #for sentence in predict_sentence :

    #    r1 = test.predict(sentence)
    #    r0 = predict_result[index]
    #    print "PREDICT: %.04f, ORIG: %d, %s" % (r1, r0, sentence)

    #    index += 1
