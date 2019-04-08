#!/usr/bin/env python
# coding: utf-8
import json

from flask import Blueprint, request
content_blueprint = Blueprint('content', __name__, url_prefix='/content')
import distance
import pymysql.cursors
import time

local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 连接数据库

# print(strings)



@content_blueprint.route('', methods=['GET', 'POST'])
def fun1():
    connect = pymysql.Connect(
        host='154.8.214.203',
        port=3306,
        user='ai_dev',
        passwd='dev2018@centerai.cn',
        db='ccc_data',
        charset='utf8'
    )

    # 输入文本
    w = request.args.get('words', None)

    # 获取游标
    cursor = connect.cursor()

    # 取得医院ID
    hid = request.args.get('hid', None)

    # 取得科室
    keshi = request.args.get('keshi', None)

    sql = "SELECT * FROM b_chat_free WHERE type=0"


    flag = False

    # 查库结果
    strings = []

    # 查相思句结果
    results = []

    if hid:
        sql += " and hid in(0,"+hid+")"
    else:
        sql += " and hid=0"


    if keshi:
        sql1 = sql + " and keshi='"+keshi+"'"
        cursor.execute(sql1)
        for tup in cursor.fetchall():
            strings.append(tup[2])
        if strings==[]:
            flag = True
        else:
            results = list(filter(lambda x: edit_distance(x, w) < 10, strings))
            if len(results) == 0:
                flag = True
            else:
                print('-'*100)
                print(results)

    if keshi==None or keshi=='' or flag==True:
        sql += " and (keshi is null or keshi='')"
        cursor.execute(sql)
        for tup in cursor.fetchall():
            strings.append(tup[2])
        results = list(filter(lambda x: edit_distance(x, w) <= 1, strings))
    result = {'result': list(results)}
    result0 = {'result':[]}
    # print 111


    if len(results) == 0:
        return json.dumps(result0, ensure_ascii=False)
    elif len(results) ==1:
        return json.dumps(result, ensure_ascii=False)
    else:
        result2 = {'result': results[0]}
        return json.dumps(result2, ensure_ascii=False)
def edit_distance(s1, s2):
    s3 = s2.decode('utf-8')

    return distance.levenshtein(s1, s3)



