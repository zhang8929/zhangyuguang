# coding: utf-8
from py2neo import Node, Relationship, Graph
from pandas import DataFrame
import json
# import codecs
import re


def qmjk_zz():
    L=[]

    with open('全民健康.json', 'r',encoding='utf-8') as f:
        contents = f.read()
        l = json.loads(contents)
        # print(len(l))
        # print(l[17])

    for i in l:
        d={}
        d['名称'] = i.get('症状名称', '')  # str
        # d['别称'] = ''.join(i.get('别名', ['暂无数据'])).replace('，', ',').split(',')  # list
        # d['英文名'] = i.get('英文名', '暂无数据')  # str
        d['定义'] = i.get('症状介绍', '暂无数据').replace('\n\t\t\t\t', '').replace('\r', '').replace('\'', ' ')  # str
        d['科室'] = list(i.get('症状科室', ['暂无数据']))  # list
        d['部位'] = i.get('症状部位', '暂无数据')  # str
        d['疾病'] = list(i.get('相关疾病', ['暂无数据']))  # list
        if d not in L:
            L.append(d)

    jsqmjk = json.dumps(L, ensure_ascii=False)

    with open('qmjkzz_new.json', 'wb') as ff:
        ff.write(jsqmjk.encode('utf-8'))

    with open('qmjkzz_new.json', 'r', encoding='utf-8') as f:  # 需要手动去除\\,和F(ab')
        content = f.read()
        l4 = json.loads(content)
        print(len(l4))
        print(l4[5])


# qmjk_zz()


def bmcx_jb():
    L=[]

    with open('jbzz.json', 'r',encoding='utf-8') as f:
        contents = f.read()
        l = json.loads(contents)
        # print(len(l))
        # print(l[17])

    for i in l:
        d={}
        d['名称'] = i.get('sick_name', '').split('(')[0]  # str
        d['定义'] = i.get('简介', '暂无数据').replace('    ', '').replace('\'', ' ')   # str
        d['科室'] = i.get('就诊科室', '暂无数据').split(',')  # list
        d['部位'] = list(i.get('所属部位', ['暂无数据']))  # list
        d['症状'] = i.get('症状体征', '暂无数据').split(',')  # list
        if d not in L:
            L.append(d)

    jsbmcx = json.dumps(L, ensure_ascii=False)

    with open('bmcxjb_new.json', 'wb') as ff:
        ff.write(jsbmcx.encode('utf-8'))

    with open('bmcxjb_new.json', 'r', encoding='utf-8') as f:  # 需要手动去除\\,和F(ab')
        content = f.read()
        l4 = json.loads(content)
        print(len(l4))
        print(l4[5])

# bmcx_jb()

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

def bmcxjb_import():
    with open('bmcxjb_new.json', 'r', encoding='utf-8') as f:
        content = f.read()
        l = json.loads(content)
    for b in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="疾病", property_key="名称", property_value=b['名称'])
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n:便民查询" % (b['名称'])
            graph.run(sql)
            if a.get('定义','暂无数据')=='暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.定义='%s'" % (b['名称'], b['定义'])
                graph.run(sql)
        else:  # 如果不存在该疾病节点，则新建节点
            # 创建疾病节点
            node_jb = Node('疾病', '便民查询', 定义=b['定义'], 名称=b['名称'])
            graph.merge(node_jb)

        # 更新科室
        for ks in b['科室']:
            if ks != '暂无数据':
                sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
                m = graph.run(sql).data()
                if m:  # 存在这个科室的节点
                    sql = "MATCH (n:`科室`{名称:'%s'}) set n:便民查询" % (ks)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_ks = Node('科室', '便民查询', 名称=ks)
                    graph.merge(node_ks)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '科室', b['名称'], ks, '科室', '科室')
                graph.run(query)

        # 更新部位
        for bw in b['部位']:
            if bw != '暂无数据':
                sql = "MATCH (n:`部位`{名称:'%s'}) RETURN n.名称" % (bw)
                m = graph.run(sql).data()
                if m:  # 存在这个部位的节点
                    sql = "MATCH (n:`部位`{名称:'%s'}) set n:便民查询" % (bw)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_bw = Node('部位', '便民查询', 名称=bw)
                    graph.merge(node_bw)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '部位', b['名称'], bw, '部位', '部位')
                graph.run(query)

        # 更新症状
        for zz in b['症状']:
            if zz != '暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称" % (zz)
                m = graph.run(sql).data()
                if m:  # 存在症状的节点
                    sql = "MATCH (n:`症状`{名称:'%s'}) set n:便民查询" % (zz)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_zz = Node('症状', '便民查询', 名称=zz)
                    graph.merge(node_zz)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '症状', b['名称'], zz, '症状', '症状')
                graph.run(query)
bmcxjb_import()

def qmjkzz_import():
    with open('qmjkzz_new.json', 'r', encoding='utf-8') as f:
        content = f.read()
        l = json.loads(content)
    for z in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="症状", property_key="名称", property_value=z['名称'])
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`症状`{名称:'%s'}) set n:全民健康" % (z['名称'])
            graph.run(sql)
            if a.get('定义','暂无数据')=='暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) set n.定义='%s'" % (z['名称'], z['定义'])
                graph.run(sql)
        else:  # 如果不存在该疾病节点，则新建节点
            # 创建疾病节点
            node_zz = Node('症状', '全民健康', 定义=z['定义'], 名称=z['名称'])
            graph.merge(node_zz)

        # 更新科室
        for ks in z['科室']:
            if ks != '暂无数据':
                sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
                m = graph.run(sql).data()
                if m:  # 存在这个科室的节点
                    sql = "MATCH (n:`科室`{名称:'%s'}) set n:全民健康" % (ks)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_ks = Node('科室', '全民健康', 名称=ks)
                    graph.merge(node_ks)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '科室', z['名称'], ks, '科室', '科室')
                graph.run(query)

        # 更新部位
        # for bw in b['部位']:
        bw = z.get('部位','暂无数据')
        if bw != '暂无数据':
            sql = "MATCH (n:`部位`{名称:'%s'}) RETURN n.名称" % (bw)
            m = graph.run(sql).data()
            if m:  # 存在这个部位的节点
                sql = "MATCH (n:`部位`{名称:'%s'}) set n:全民健康" % (bw)
                graph.run(sql)
            else:  # 不存在该节点
                node_bw = Node('部位', '全民健康', 名称=bw)
                graph.merge(node_bw)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '症状', '部位', z['名称'], bw, '部位', '部位')
            graph.run(query)

        # 更新疾病
        for jb in z['疾病']:
            if jb != '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (jb)
                m = graph.run(sql).data()
                if m:  # 存在症状的节点
                    sql = "MATCH (n:`疾病`{名称:'%s'}) set n:全民健康" % (jb)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_jb = Node('疾病', '全民健康', 名称=jb)
                    graph.merge(node_jb)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '症状', jb ,z['名称'], '症状', '症状')
                graph.run(query)

qmjkzz_import()