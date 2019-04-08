#!/usr/bin/env python
# coding: utf-8

import time
from flask import Flask,request
import json
import requests
import sys, os
# import modules & set up logging
import gensim, logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 实例flask对象
app = Flask(__name__)

# 模板路径
model_dir  = os.path.dirname(os.path.realpath(__file__)) + '/../models'
model_path = "%s/%s" % (model_dir, '2018121301.bin')

# model_path = '../models/2018121301.bin'

# 模板读取
model = gensim.models.Word2Vec.load(model_path)


# 设置路由
@app.route('/', methods=['GET', 'POST'])
def find_words():
    # 获取地址参数--查询用词
    url_keyword = request.args.get('search', None)
    if url_keyword is None:
        return ""
    else:
        url_keyword = url_keyword.encode('utf-8')
        keyword = url_keyword

        # 获取地址参数--查询数量设置
        url_limit = request.args.get('limit', None)
        if url_limit is None:
            url_limit = 10
        else:
            url_limit = url_limit.encode('utf-8')
            url_limit = int(url_limit)

        # 获取地址参数---相似度设置
        url_similar = request.args.get('similar', None)
        if url_similar is None:
            url_similar = 0.5
        else:
            url_similar = url_similar.encode('utf-8')
            url_similar = float(url_similar)

    n = url_limit
    try:
        rs = model.wv.most_similar([keyword], topn=n)
        words_list = []
        for (w, s) in rs :
            words_dic = {}
            if s >= url_similar:
                words_dic["words"] = w
                words_dic["similar"] = s

                words_list.append(words_dic)

        z_dic = {}
        # words_list2作为值加入字典，为后面转json格式准备
        z_dic["keys"] = words_list
        # 字典转json格式
        json_dic = json.dumps(z_dic)
        return json_dic
		
    except:

        return ""



if __name__ == '__main__':
    # 开启程序
    app.run(host='0.0.0.0', port='1213', debug=True)
