#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

LTP_DATA_DIR = '/Users/yangxl/Source/LTP/ltp_data_v3.4.0'
# 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')
# 依存句法分析模型路径，模型名称为`parser.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
# 分词模型路径，模型名称为`cws.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
# 自定义分词词典
my_dict_path  = os.path.dirname(os.path.realpath(__file__)) \
                + '/../dict/LTP_dict_medicine.txt';


from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, my_dict_path)
#segmentor.load(cws_model_path)
words = segmentor.segment('每天晚上肚子疼')
print '\t'.join(words)
segmentor.release()
sys.exit(0)


#words = ['元芳', '你', '怎么', '看']
#postags = ['nh', 'r', 'r', 'v']
words = ['我', '是', '中国', '人']
postags =  ['r', 'v', 'ns', 'n']

from pyltp import Parser
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型

from pyltp import SementicRoleLabeller
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(srl_model_path)  # 加载模型

# arcs 使用依存句法分析的结果
arcs = parser.parse(words, postags)  # 句法分析
roles = labeller.label(words, postags, arcs)  # 语义角色标注

# 打印结果
for role in roles:
    print role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
labeller.release()  # 释放模型
