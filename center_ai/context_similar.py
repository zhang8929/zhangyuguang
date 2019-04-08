#!/usr/bin/env python
# coding: utf-8
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pymysql
from flask import Flask,request,jsonify,Blueprint
import json
app=Flask(__name__)

context_blueprint = Blueprint('context', __name__, url_prefix='/context')

def get_data():
    host= '154.8.214.203'
    user= 'ai_dev'
    password = 'dev2018@centerai.cn'
    db = 'ccc_data'
    db = pymysql.connect(host, user, password, db)
    cursor = db.cursor()
    sql = """select content from b_chat_free """
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

def get_data1(keshi):
    host= '154.8.214.203'
    user= 'ai_dev'
    password = 'dev2018@centerai.cn'
    db = 'ccc_data'
    db = pymysql.connect(host, user, password, db)
    cursor = db.cursor()
    sql = """select content from b_chat_free where keshi='{}' """.format(keshi)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

def takeSecond(f):
    return f[1]


def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1 = s1.encode('utf-8').replace('吗', '').replace('呢', '').replace('?', '')
    a = s1.decode('utf-8')
    s1, s2 = add_space(a), add_space(s2.decode('utf-8'))
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1,s2]

    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    res = 1.0 * numerator / denominator
    return "%.3f" % res

@context_blueprint.route('/',methods=['GET','POST'])
def res():
    res = []
    word = request.args.get('words',None)
    keshi = request.args.get('keshi',None)
    if keshi == None:

        data = get_data()
        for dd in data:
            print(dd[0])
            value = jaccard_similarity(word,dd[0])
            # print(type(value))
            if float(value) < 0.25:
                continue
            tmp = (dd[0],value)
            res.append(tmp)

        res.sort(key=takeSecond, reverse=True)
        # print res
        if len(res)>=1:
            return jsonify(res=res[0])

        else:
            return jsonify(res = [''])
    else:
        data = get_data1(keshi)
        for dd in data:
            print(dd[0])
            value = jaccard_similarity(word, dd[0])
            # print(type(value))
            if float(value) < 0.25:
                continue
            tmp = (dd[0], value)
            res.append(tmp)

        res.sort(key=takeSecond, reverse=True)
        # print res
        if len(res) >= 1:
            return jsonify(res=res[0])

        else:
            return jsonify(res=[''])

