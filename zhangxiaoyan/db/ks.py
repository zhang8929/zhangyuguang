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

def wsks():

    sql = "MATCH (n:`症状`)-[r:科室]->(m:`科室`) where m.名称 contains '、' return n.名称,m.名称"
    # sql = "MATCH (n:`疾病`)-[r:科室]->(m:`科室`) where m.名称 contains '、' return n.名称,m.名称"
    m = graph.run(sql).data()
    # print(m)
    for i in m:
        zzname = i['n.名称']
        ksl = i['m.名称'].split('、')#列表
        for ks in ksl:
            if ks != '暂无数据':
                sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
                m = graph.run(sql).data()
                if m:  # 存在这个科室的节点
                    sql = "MATCH (n:`科室`{名称:'%s'}) set n:三九" % (ks)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_ks = Node('科室', '三九', 名称=ks)
                    graph.merge(node_ks)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '科室', zzname, ks, '科室', '科室')
                graph.run(query)

wsks()