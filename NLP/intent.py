#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import jieba
import jieba.posseg as pseg
from semantics.reduce import WordsReduce

jieba.load_userdict("dict/LTP_dict_medicine.txt")
jieba.load_userdict("dict/vr.txt")

wReduce = WordsReduce()

text = ('雄激素高是什么病',
    '年轻人偶尔心绞痛怎么治疗',
    '他有家族性侏儒病史',
    '小便尿血是怎么回事')

def process_text (text) :
    words = pseg.cut(text)
    orig_words = []
    for x, y  in words:
        orig_words.append((x,y))
    opts_words = wReduce.reduce(orig_words)
    
    orig_tens  = []
    opts_tens  = []
    
    for word, flag in orig_words :
        orig_tens.append("%s[%s]" % (word, flag))
    
    for word, flag in opts_words :
        opts_tens.append("%s[%s]" % (word, flag))
    
    print "\n原始句: %s\n----------------" % (text)
    print "分词后", " / ".join(orig_tens)
    print "精简后", " / ".join(opts_tens)


for t in text :
    process_text(t)
