#!/usr/bin/env python3
# coding: utf-8
# File: sentence_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-10

import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
import jieba
import jieba.posseg as pseg
from semantics.postag import PosTagMapping

jieba.load_userdict("LTP_dict_medicine.txt")
mapping = PosTagMapping()

class LtpParser:
    def __init__(self):
        LTP_DIR = "../../ltp_data_v3.4.0"
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))#分词

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))#词性标注

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))#依存句法

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))#实体命名

        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl.model'))#语义角色标注

    '''语义角色标注'''
    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name:[arg.name,arg.range.start, arg.range.end] for arg in role.arguments}
        return roles_dict

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def build_parse_child_dict(self, words, postags, arcs):
        child_dict_list = []
        format_parse_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index].head == index+1:   #arcs的索引从1开始
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id然  #[3,3,0,3]
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1].decode('utf-8') for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            # ['SBV', '我', 0, 'r', '感到', 2, 'v']
            a = [relation[i], words[i].decode('utf-8'), i, postags[i], heads[i], rely_id[i]-1, postags[rely_id[i]-1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list

    '''parser主函数'''
    def parser_main(self, sentence):
        # words = list(self.segmentor.segment(sentence))
        # words = list(pseg.cut(sentence))
        wordspsegs = pseg.cut(sentence)
        words = []
        postags = []
        vWords = []
        for word, tag in wordspsegs:
            vWords.append("%s/%s" % (word, tag))
            ltpTag = mapping.jieba2LTP(tag)
            words.append(word.encode('utf8'))
            postags.append(ltpTag.encode('utf8'))
        # postags = list(self.postagger.postag(words))
        arcs = self.parser.parse(words, postags)
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list,vWords,arcs


if __name__ == '__main__':
    parse = LtpParser()
    sentence = '他感到很头晕'
    words, postags, child_dict_list, roles_dict, format_parse_list,vWords,arcs = parse.parser_main(sentence)
    print(vWords, len(words))
    # print([i for i in arcs])
    print(postags, len(postags))
    print(child_dict_list, len(child_dict_list))
    print(roles_dict)
    print(format_parse_list, len(format_parse_list))