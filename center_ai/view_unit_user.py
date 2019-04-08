#!/usr/bin/env python
# coding: utf-8
import json

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pymysql
import gensim
import requests
import os
import jieba.posseg as psg

from flask import Flask,request,jsonify,Blueprint
app=Flask(__name__)

unit_user_blueprint = Blueprint('unit_user', __name__, url_prefix='/unit_user')

train_dir  ='/Users/zhangyuguang/Documents/data';
# train_dir  ='/mnt/flask/new_models';
#
train_path = "%s/%s" % (train_dir, '0404_user.txt')
print train_path
model_dir = '/Users/zhangyuguang/Documents/model';
# model_dir = '/mnt/flask/new_models';


docs = {}
with open(train_path,'r') as fh :
    index = 0
    for line in fh :
        l = line.strip()
        docs[index] = l
        index += 1
    fh.close()

model_name = "0404sentew_100d_w15_m1_e400.bin"
# model_name = 'docmodel'

#model_name = "800w_100d_w15_m1_e800.bin"
model_path = "%s/%s" % (model_dir, model_name)
print model_path
model_dm = gensim.models.Doc2Vec.load(model_path)


'''
找相似句
'''
@unit_user_blueprint.route('', methods=['GET', 'POST'])
def test():

    words = (request.args.get('words').encode('utf-8'))
    words = ((words).replace("'", '').split(' '))
    #获得对应的输入句子的向量
    inferred_vector_dm = model_dm.infer_vector(doc_words=words)
    # inferred_vector_dm = model_dm.infer_vector(doc_words=words, alpha=0.025, steps=500)
    #返回相似的句子

    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=1)

    print "ORIG: %s\n--------" % ''.join(words)
    res = []
    for (i, sim) in sims :
        res.append([i,sim,docs[i]])
        print res
    if res[0][1] < 0.1:
        ret = ''
        result = {'result': ret}
        # print "%d, %.04f, %s" % (i, sim, docs[i])
        # return "USED TIME: %.03f" % (t1 - t0)
        return json.dumps(result, ensure_ascii=False)
    else:

        connect = pymysql.Connect(
            host='154.8.214.203',
            port=3306,
            user='ai_dev',
            passwd='dev2018@centerai.cn',
            db='ccc_data',
            charset='utf8'
        )

        # 获取游标
        cursor = connect.cursor()

        # 取出被标记为未更新的内容
        sql = "SELECT question,aswer,Level_1_department,Level_2_department FROM faq_user WHERE fenci_q="+"'"+res[0][2]+"'"
        print sql

        cursor.execute(sql)
        # print (cursor.fetchall())
        # strings = []
        # if len(cursor.fetchall())==1:
        #     for tup in cursor.fetchall():
        #         # print tup
        #         strings.append(tup)
            # print len(strings)
        # print len(cursor.fetchone())
        result = {'result':cursor.fetchone()}
            # print "%d, %.04f, %s" % (i, sim, docs[i])
            # return "USED TIME: %.03f" % (t1 - t0)
        return json.dumps(result, ensure_ascii=False)
