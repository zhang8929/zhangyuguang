# coding: utf-8

'''
分词
'''

import os
import jieba
import jieba.posseg as pseg
from reduce import WordsReduce


class ChineseWordSplit(object) :

    __words = []
    __reduced_words = []

    def __init__(self) :

        user_dict = os.path.dirname(os.path.realpath(__file__)) +\
            '/../dict/JIEBA_medicine_1213.txt'

        jieba.load_userdict(user_dict)

    # 结巴分词
    def split_by_jieba (self, text):

        self.__words = []
        xs = pseg.cut(text)

        for word, tag  in xs :
            self.__words.append((word, tag))

        return self.__words

    def text_to_sequence(self, text) :

        cuts = jieba.cut(text)
        return cuts

    def debug_split (self, prefix = '[JIEBA]'):

        vs = []
        for word, tag in self.__words :
            vs.append("%s/%s" % (word, tag))
        print prefix, '  '.join(vs)

    def reduce (self) :

        wReduce = WordsReduce()
        self.__reduced_words = wReduce.reduce(self.__words)
        return self.__reduced_words

    def debug_reduce(self, prefix = '[REDUS]') :

        vs = []
        for a, b in self.__reduced_words :
            vs.append("%s/%s" % (a, b))
        print "[REDUS]", '  '.join(vs)

