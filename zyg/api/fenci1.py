#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,request
# import sys

import json
import jieba

import jieba.posseg as psg

jieba.load_userdict("/tmp/test.txt")

app = Flask(__name__)


@app.route('/index', methods=['GET','POST'])
def fun():
    w = request.args.get('words', None)

    # cut = jieba.cut(w)
    list1 = []
    for (word, flag) in psg.cut(w):
        list1.append((word, flag))
    # print(list1)
    result = {'result': list1}

    # :



    # a =  psg.cut(w)
    # for i in a :
    #     print(i)


    return json.dumps(result,ensure_ascii=False)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9999', debug=True)
