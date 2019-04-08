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

import sys
sys.path.insert(0, '..')
from semantics.cws import ChineseWordSplit
from semantics.dependency_parsing import semanticsDP
from database.body_regions import BodyRegions
from semantics.node import SemanticsNode


class Intention (object) :

    __cws = None
    __dp  = None
    __DEBUG = False
    __words = []
    __tags  = []
    __rely_id = []
    __relation = []
    __heads    = []

    def __init__ (self, debug = False) :
        self.__cws = ChineseWordSplit()
        self.__dp  = semanticsDP()
        self.__DEBUG = debug
        self.__regions = BodyRegions()

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
        self.__rely_id = rely_id
        self.__relation = relation
        self.__heads = heads

        # 寻找部位和"伴有"这些关键词
        relyId  = 1
        indexId = 0
        maps = []
        for w in self.__words :
            if w == '伴有' or self.__regions.is_body_region(w) :
                node = self.__build_map_node (indexId, relyId, None)
                maps.append(node)

            indexId += 1
            relyId  += 1

        # 这句话没有找到关键词, 放弃处理
        if len(maps) == 0 :
            return None

        # 对每个找到的关键词，打印子节点的基于语法结构(合成)的目标词
        for node in maps :
            #_map = self.__build_map_from_keyword(k, keywords[k])
            words = node.children_words()
            print node.word, "\t", '/'.join(words)

        return None

    def __build_map_from_keyword(self, parent, pWord, pRelyId) :

        _map = {}

        # ids 寻找哪些词的rely_id与pRelyId匹配
        ids = []
        i = 0
        for id in self.__rely_id :
            if id == pRelyId:
                ids.append(i)
            i += 1

        arr_word_rel = []
        for id in ids :
            node = {}
            node.word = self.__words[id]
            node.rely_id = id + 1
            node.tag = self.__tags[id]
            node.rel = self.__relation[id]
            node.parent = parent
            node.children = []



    def __get_rel_by_keyword(self, pWord, pTag, rely_id, isSub = False) :

        ids = []
        i = 0
        for id in self.__rely_id :
            if id == rely_id:
                #tag = self.__tags[i]
                #if tag not in ('x', 'd') :
                    ids.append(i)
            i += 1

        arr_word_rel = []
        for id in ids :
            word = self.__words[id]
            my_rely_id = id + 1
            my_tag     = self.__tags[id]
            my_relation= self.__relation[id]


            # 若在子处理流程中，对词语做连接
            if isSub and pTag not in ('x', 'd') :
                if my_relation in ( 'ATT', 'COO', 'LAD') :
                    word = word + pWord
                elif my_relation in ('RAD' ) :
                    word = pWord + word

            ws = self.__get_rel_by_keyword(word, my_tag, my_rely_id, True)
            print word, my_rely_id,  my_tag, my_relation
            if my_tag not in ('x', 'd') :
                arr_word_rel.append((word, my_relation))
            for w in ws :
                arr_word_rel.append(w)

        return arr_word_rel

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


    def __build_map_node (self, indexId, pRelyId, parent = None) :

        node = SemanticsNode()
        node.word = self.__words[indexId]
        node.index_id = indexId
        node.rely_id = pRelyId
        node.tag = self.__tags[indexId]
        node.relation = self.__relation[indexId]
        node.parent = parent
        node.children = []

        # ids 寻找哪些词的rely_id与pRelyId匹配
        ids = []
        i = 0
        for id in self.__rely_id :
            if id == pRelyId:
                ids.append(i)
            i += 1

        arr_word_rel = []
        for id in ids :
            sIndexId = id
            sRelyId = id + 1
            sNode = self.__build_map_node(sIndexId, sRelyId, node)
            node.children.append(sNode)

        return node
