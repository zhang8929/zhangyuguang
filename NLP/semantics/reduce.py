#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
# 词性表
词性	含义	词性	含义	词性	含义	词性	含义
n	普通名词
f	方位名词
s	处所名词
t	时间名词
nr	人名
ns	地名
nt	机构团体名
nw	作品名
nz	其他专名
v	普通动词
vd	动副词
vn	名动词
a	形容词
ad	副动词
an	名形词
d	副词
m	数量词
q	量词
r	代词
p	介词
c	连词
u	助词
xc	其他虚词
w	标点符号
l   习用语
'''

class WordsReduce(object):

    __dicts = None

    def __init__ (self) :

        # 人名不保留
        self.__dicts = ('n','f','s','t','ns','nt', 'nw', 'nz',\
                'nr', 'jb', 'zz', 'yp', 'ks',\
                'v', 'vd', 'vn', 'vr', \
                #'a', 'ad', 'an',  \
                'l',
                )

    def reduce(self, word_list) :

        seqs = []

        for word, flag in word_list :
            if flag in self.__dicts :
                seqs.append((word, flag))

        return seqs
