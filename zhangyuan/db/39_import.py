# coding: utf-8

from py2neo import Node, Relationship, Graph
from pandas import DataFrame
import json
import codecs


# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123")
# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="m4eeee")

with codecs.open('39jk_new.json', 'r',encoding='utf-8') as f:
    contents = f.read()
    l = json.loads(contents)
    # print(len(l))
    # print(l[18])

with open('zz39_new.json', 'r', encoding='utf-8') as f:
    content = f.read()
    ll = json.loads(content)
    # print(ll[2])


#39库
for b in l:
    #创建疾病节点
    node_jb = Node('疾病','三九',病因=b['病因'], 别称=b['别称'],英文名=b['英文名'],温馨提示=b['温馨提示'],患病比例=b['患病比例'],
                   定义=b['定义'],名称=b['名称'],治疗费用=b['治疗费用'],多发人群=b['多发人群'],患病比例值=-1,
                   医保=b['医保'],传染性=b['传染性'],治疗周期=b['治疗周期'],治愈率=b['治愈率'],治愈率值=b['治愈率值'])
    graph.merge(node_jb)
    #创建治疗方式节点并建立关系
    for a in b['治疗方法']:
        if a != '暂无数据':
            node_zlff = Node('治疗方法','三九', 名称=a)
            graph.merge(node_zlff)
            query1 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '治疗方法', b['名称'], a,'治疗方法', '治疗方法')
            graph.run(query1)

    # 创建症状节点并建立关系
    for z in b['症状']:
        if z != '暂无数据':
            node_zz = Node('症状','三九', 名称=z)
            graph.merge(node_zz)
            query2 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '症状', b['名称'], z,'症状', '症状')
            graph.run(query2)

    # 创建科室节点并建立关系
    for k in b['科室']:
        if k != '暂无数据':
            node_ks = Node('科室','三九', 名称=k)
            graph.merge(node_ks)
            query3 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '科室', b['名称'], k, '科室','科室')
            graph.run(query3)
    # 创建部位节点并建立关系
    for bw in b['部位']:
        if bw != '暂无数据':
            node_bw = Node('部位','三九', 名称=bw)
            graph.merge(node_bw)
            query5 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '部位', b['名称'], bw, '部位', '部位')
            graph.run(query5)
    # 创建药品节点并建立关系
    for y in b['药品']:
        if y != '暂无数据':
            node_yp = Node('药品','三九', 名称=y)
            graph.merge(node_yp)
            query4 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '药品', b['名称'], y,'药品', '药品')
            graph.run(query4)
    # 创建传播途径节点并建立关系
    for c in b['传播途径']:
        if c != '无' and c != '暂无数据':
            node_cbtj = Node('传播途径','三九', 名称=c)
            graph.merge(node_cbtj)
            query6 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '传播途径', b['名称'], c, '传播途径', '传播途径')
            graph.run(query6)
    # 创建检查节点并建立关系
    for j in b['检查项目']:
        if j != '暂无数据':
            node_jc = Node('检查项目','三九', 名称=j)
            graph.merge(node_jc)
            query7 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '检查项目', b['名称'], j, '检查项目', '检查项目')
            graph.run(query7)


for b in l:
# 创建并发疾病关系
    for jb in b['并发疾病']:
        if jb != '暂无数据':
            query8 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '疾病', b['名称'], jb,'并发疾病', '并发疾病')
            graph.run(query8)

#症状库
for z in ll:
    #更新或创建症状节点
    sql1 = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称"%(z['名称'])
    a = graph.run(sql1).data()
    if a:#更新
        sql2 = "MATCH (n:`症状`{名称:'%s'}) set n.图片='%s',n.别名='%s',n.定义='%s' " % (z['名称'],z['图片'],z['别名'],z['定义'])
        graph.run(sql2)
    else:#创建
        node_zz = Node('症状','三九', 图片=z['图片'], 别名=z['别名'],定义=z['定义'], 名称=z['名称'])
        graph.merge(node_zz)
    #检查项目
    for jc in z['检查']:
        # sql = "MATCH (n:`检查项目`{名称:'%s'}) RETURN n.名称" % (jc)
        # m = graph.run(sql).data()
        # if m:
        #     query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #         '症状', '检查项目', z['名称'], jc, '检查项目', '检查项目')
        #     graph.run(query)
        # else:
        if jc != '暂无数据':
            node_jc = Node('检查项目','三九', 名称=jc)
            graph.merge(node_jc)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '症状', '检查项目', z['名称'], jc, '检查项目', '检查项目')
            graph.run(query)
    #科室
    for ks in z['科室']:
        # sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
        # m = graph.run(sql).data()
        # if m:
        #     query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #         '症状', '科室', z['名称'], ks, '科室', '科室')
        #     graph.run(query)
        # else:
        if ks != '暂无数据':
            node_ks= Node('科室','三九', 名称=ks)
            graph.merge(node_ks)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '症状', '科室', z['名称'], ks, '科室', '科室')
            graph.run(query)
    #药品
    for yp in z['药品']:
        # sql = "MATCH (n:`药品`{名称:'%s'}) RETURN n.名称" % (yp)
        # m = graph.run(sql).data()
        # if m:
        #     query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #         '症状', '药品', z['名称'], yp, '药品', '药品')
        #     graph.run(query)
        # else:
        if yp != '暂无数据':
            node_yp = Node('药品','三九', 名称=yp)
            graph.merge(node_yp)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '症状', '药品', z['名称'], yp, '药品', '药品')
            graph.run(query)
    # 部位
    for bw in z['部位']:
        # print(bw)
        # sql = "MATCH (n:`部位`{名称:'%s'}) RETURN n.名称" % (bw)
        # m = graph.run(sql).data()
        # if m:
        #     query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #         '症状', '部位', z['名称'], bw, '部位', '部位')
        #     graph.run(query)
        # else:
        if bw != '暂无数据':
            node_bw = Node('部位','三九', 名称=bw)
            graph.merge(node_bw)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '症状', '部位', z['名称'], bw, '部位', '部位')
            graph.run(query)

    # 疾病
    for jb in z['疾病']:
        sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (jb)
        m = graph.run(sql).data()
        if not m:
        #     query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #         '疾病', '症状', jb,z['名称'], '症状', '症状')
        #     graph.run(query)
        # else:
            node_jb = Node('疾病','三九', 名称=jb)
            graph.merge(node_jb)
        query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
            '疾病', '症状', jb, z['名称'], '症状', '症状')
        graph.run(query)

for z in ll:
    # 创建相似症状关系
    for zz in z['相似症状']:
        if zz != '暂无数据':
            query8 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '症状', '症状', z['名称'], zz, '相似症状', '相似症状')
            graph.run(query8)


# # for b in l:
# #     sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
# #     m = graph.run(sql).data
# #     if m:  # 更新
# #         if b['治愈率值']==None:
# #             sql2 = "MATCH (n:`疾病`{名称:'%s'}) set n.治愈率='%s',n.治愈率值=-1 " % (b['名称'],b['治愈率'])
# #             graph.run(sql2)
# #         else:
# #             sql2 = "MATCH (n:`疾病`{名称:'%s'}) set n.治愈率='%s',n.治愈率值=%s " % (b['名称'], b['治愈率'], b['治愈率值'])
# #             graph.run(sql2)
#
# for b in l:
#     sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
#     m = graph.run(sql).data()
#     if m:  # 更新
#         sql2 = "MATCH (n:`疾病`{名称:'%s'}) set n.治愈率值=%s,n.患病比例值=-1 " % (b['名称'],b['治愈率值'])
#         graph.run(sql2)