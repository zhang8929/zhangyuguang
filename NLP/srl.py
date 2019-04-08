#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

LTP_DATA_DIR = '/Users/yangxl/Source/LTP/ltp_data_v3.4.0'
# 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')
# 依存句法分析模型路径，模型名称为`parser.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
# 分词模型路径，模型名称为`cws.model`
#cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

import jieba
import jieba.posseg as pseg
from postag import PosTagMapping

jieba.load_userdict("dict/LTP_dict_medicine.txt")
mapping = PosTagMapping()

text = '雄激素高是什么病'
text = '他有家族性侏儒病史'
text = '九个月宝宝睡觉头上出很多汗怎么办'
text = '三精葡萄糖酸钙锌口服溶液蓝瓶疗效更好吗'


xs = pseg.cut(text)
words = []
postags = []
vWords = []
for word, tag  in xs :
    vWords.append("%s/%s" % (word, tag))
    ltpTag = mapping.jieba2LTP(tag)
    words.append(word.encode('utf8'))
    postags.append(ltpTag.encode('utf8'))

print text
print "[JIEBA]", '  '.join(vWords)


from pyltp import Parser
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

from pyltp import SementicRoleLabeller
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(srl_model_path)  # 加载模型

# arcs 使用依存句法分析的结果
#arcs = parser.parse(words, postags)  # 句法分析
#print "依存句法\n", '-'*80, "\n"
#print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)

from pyhanlp import HanLP

print(HanLP.parseDependency(text))


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
