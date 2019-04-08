#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,request
# import sys

import json
import jieba
from pyltp import SentenceSplitter

import jieba.posseg as psg


app = Flask(__name__)


@app.route('/index', methods=['GET','POST'])
def fun():
    w = request.args.get('words', None)

    # cut = jieba.cut(w)

    w = w.encode('utf-8')
    sentence = SentenceSplitter.split(w)
    list1 = []
    for i in sentence:

        list1.append(i)
    

    result = {'result':list1}


    return json.dumps(result,ensure_ascii=False)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=17239, debug=True)
