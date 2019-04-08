#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 测试依存句法分析处理

import os, sys

#from semantics.cws import ChineseWordSplit
#from semantics.dependency_parsing import semanticsDP
from semantics.intention import IntentionParser
from pyhanlp import HanLP
from database.questions import QuestionList


def  parse_CoNLL_format(s) :
    rs = {}
    ps = s.split("\n")
    for x in ps :
        words = x.split("\t")
        index = words[0]
        word = words[1]
        refer = words[6]
        ship  = words[7]
        type1 = words[3]
        type2 = words[4]

        index = int(index)
        m = {
            'word' : word,
            'index' : index,
            'refer' : refer,
            'rel'   : ship,
            'type1'  : type1,
            'type2'  : type2,
        }

        rs[index] = m

    return rs



def parse_dependency(text) :

    split_words = cws.split_by_jieba(text)
    reduced_words = cws.reduce()

    print text
    cws.debug_split()
    cws.debug_reduce()

    dp_result = dp.parse_by_LTP(split_words)
    dp.debug()
    print "\n"

    #ts = ""
    #for a, b in opts_words :
    #    ts += a

    #rs = HanLP.parseDependency(text)
    #print rs



questions = QuestionList()
question  = questions.getQuestion()
index = 0
parser = IntentionParser()

while question and index <= 10 :
    intent = parser.get_intent(question)
    question  = questions.getQuestion()
    index += 1


'''
roles = labeller.label(words, postags, arcs)  # 语义角色标注


print "SRL\n", '-'*80, "\n"
# 打印结果
for role in roles:
    print role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])

    print words[role.index]
labeller.release()  # 释放模型
'''
