#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

'''
使用LTP库对句子做依存句法分析

'''

from pyltp import Parser
from postag import PosTagMapping

class semanticsDP (object) :

    LTP_DATA_DIR = '/Users/yangxl/Source/LTP/ltp_data_v3.4.0'

    # 语义角色标注模型目录路径，模型目录为`srl`
    srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')

    # 依存句法分析模型路径，模型名称为`parser.model`
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')

    # 分词模型路径，模型名称为`cws.model`
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

    __ws = []
    __ts = []
    __orig_ts = []

    def __init__ (self) :

        self.__parser = Parser()
        self.__parser.load(self.par_model_path)


    # 使用依存句法分析句子
    def parse_by_LTP (self, split_words, convert_postag = True) :

        self.__ws = []
        self.__ts = []
        self.__orig_ts = []

        # 结巴分词的词性转LTP分词的词性
        mapping = PosTagMapping()

        for w, t in split_words :
            self.__ws.append(w.encode('utf8'))
            self.__orig_ts.append(t.encode('utf8'))
            self.__ts.append(mapping.jieba2LTP(t).encode('utf8'))

        self.__result = self.__parser.parse(self.__ws, self.__ts)
        return self.__result


    def get_words (self) :
        return self.__ws

    def get_postags (self) :
        return self.__orig_ts

    def get_mapping_postags(self):
        return self.__ts

    def debug(self, prefix = '[LTP_DP]') :

        #print prefix, "\t".join("%d:%s" % (arc.head, arc.relation) for arc in \
        #                self.__result)

        vs = []
        rely_id = [arc.head for arc in self.__result]    # 提取依存父节点id
        relation = [arc.relation for arc in self.__result]   # 提取依存关系
        heads = ['Root' if id == 0 else self.__ws[id-1] for id in rely_id]  # 匹配依存父节点词语

        for i in range(len(self.__ws)):
            vs.append("%s(%s/%s, %s)" % (relation[i], self.__ws[i],
self.__orig_ts[i], heads[i]))

        print prefix, " ".join(vs)


'''
from pyltp import SementicRoleLabeller
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(srl_model_path)  # 加载模型


from pyhanlp import HanLP

print(HanLP.parseDependency(text))


roles = labeller.label(words, postags, arcs)  # 语义角色标注


print "SRL\n", '-'*80, "\n"
# 打印结果
for role in roles:
    print role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])

    print words[role.index]
labeller.release()  # 释放模型
'''
