#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import jieba

import jieba.posseg as psg
import requests

import json

import sys

# jieba.load_userdict("/tmp/test.txt")
#
#
#
# s = '小明得了癌症'
#
# list1 = []
# for (word,flag) in psg.cut(s):
#
#     list1.append((word,flag))
# # print(list1)
# result = {'result': list1}
# ret = json.dumps(result)
#
# print ret.decode('unicode-escape')


ret = requests.get(url='http://121.40.85.88:9999/index?words=%E5%B0%8F%E6%98%8E%E5%BE%97%E4%BA%86%E7%99%8C%E7%97%87')
res = (ret.content).decode('utf-8')
a = json.loads(res)
print (type(a))
