#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
给出一句话的意图

若成功，返回意图和参数
若失败，返回None


关系类型	Tag	Description	Example
主谓关系	SBV	subject-verb	我送她一束花 (我 <– 送)
动宾关系	VOB	直接宾语，verb-object	我送她一束花 (送 –> 花)
间宾关系	IOB	间接宾语，indirect-object	我送她一束花 (送 –> 她)
前置宾语	FOB	前置宾语，fronting-object	他什么书都读 (书 <– 读)
兼语        DBL	double      他请我吃饭 (请 –> 我)
定中关系	ATT	attribute	红苹果 (红 <– 苹果)
状中结构	ADV	adverbial	非常美丽 (非常 <– 美丽)
动补结构	CMP	complement	做完了作业 (做 –> 完)
并列关系	COO	coordinate	大山和大海 (大山 –> 大海)
介宾关系	POB	preposition-object	在贸易区内 (在 –> 内)
左附加关系	LAD	left adjunct	大山和大海 (和 <– 大海)
右附加关系	RAD	right adjunct	孩子们 (孩子 –> 们)
独立结构	IS	independent structure	两个单句在结构上彼此独立
核心关系	HED	head	指整个句子的核心

'''

from pyhanlp import HanLP
from cws import ChineseWordSplit
from dependency_parsing import semanticsDP


class IntentionParser (object) :

    __cws = None
    __dp  = None
    __DEBUG = False
    __words = []
    __tags  = []

    def __init__ (self) :
        self.__cws = ChineseWordSplit()
        self.__dp  = semanticsDP()

    def get_intent (self, text) :

        split_words = self.__cws.split_by_jieba(text)
        reduced_words = self.__cws.reduce()

        self.__intent = self.__dp.parse_by_LTP(split_words)

        if self.__DEBUG :
            print text
            self.__cws.debug_split()
            self.__cws.debug_reduce()
            self.__dp.debug()
            print "\n"

        return self.__parse_intent ()

    def __parse_intent (self) :

        rs = self.__intent
        self.__words = self.__dp.get_words()
        self.__tags  = self.__dp.get_postags()

        rely_id = [arc.head for arc in rs]    # 提取依存父节点id
        relation = [arc.relation for arc in rs]   # 提取依存关系
        heads = ['Root' if id == 0 else self.__words[id-1] for id in rely_id]  # 匹配依存父节点词语

        if len(self.__words) > 5:
            return None

        hed = self.__get_hed()

        # 规则1 若宾语是药. 主语含有疾病  则是找药品
        if self.__is_query_zhiliao(hed):
            return self.__intent_zhiliao()
        elif self.__is_query_zhengzhuang(hed):
            return self.__intent_zhengzhuang()
        else :
            print hed
            self.__dp.debug()

    def __get_hed (self) :

        index = 0
        for x in self.__intent :
            if x.relation == 'HED' :
                return self.__words[index]
            index += 1


    def __is_query_zhiliao(self, keyword) :
        keys = ['治疗', '怎么办', '怎么回事', '怎么弄']
        for k in keys :
            if keyword.find(k) >= 0 :
                return True
        return False

    def __intent_zhiliao(self) :
        pass

    def __is_query_zhengzhuang(self, keyword):
        keys = ['表现', '症状', '特征']
        for k in keys :
            if keyword.find(k) >= 0 :
                return True
        return False

    def __intent_zhengzhuang(self):
        pass
