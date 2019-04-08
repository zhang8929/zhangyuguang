# coding: utf-8
from py2neo import Node, Relationship, Graph
from pandas import DataFrame
import json
# import codecs
import re

# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123")
graph = Graph(
            host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="m4eeee")


def jbk_jb():
    L=[]
    with open('疾病库疾病.json', 'r',encoding='utf-8') as f:
        contents = f.read()
        l = json.loads(contents)
        # print(len(l))
        # print(l[17])

    for b in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="疾病", property_key="名称", property_value=b['sick_name'])
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n:疾病库" % (b['sick_name'])
            graph.run(sql)
            if a.get('图片','暂无数据')=='暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.图片='%s'" % (b['sick_name'], b.get('img_url','暂无数据'))
                graph.run(sql)


# jbk_jb()

def qy_zz():
    L=[]
    with open('qiuyizz.json', 'r',encoding='utf-8') as f:
        contents = f.read()
        l = json.loads(contents)
        # print(len(l))
        # print(l[17])

    for b in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="症状", property_key="名称", property_value=b['症状名称'])
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`症状`{名称:'%s'}) set n:求医" % (b['症状名称'])
            graph.run(sql)
            if a.get('别名','暂无数据')=='暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) set n.别名='%s'" % (b['症状名称'], b.get('别名','暂无数据'))
                graph.run(sql)

qy_zz()