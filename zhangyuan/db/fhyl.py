# coding: utf-8
from py2neo import Node, Relationship, Graph
from pandas import DataFrame
import json
# import codecs
import re


def yl_jb():
    L=[]
    with open('有来.json', 'r',encoding='utf-8') as f:
        contents = f.read()
        l = json.loads(contents)
        # print(len(l))
        # print(l[17])

    for i in l:
        d={}
        d['科室'] =[]
        ghks= list(i.get('挂号科室', ['暂无数据']))  # list
        for ks in ghks:
            ks = ks.split(' ')[0]
            if ks not in d['科室']:
                d['科室'].append(ks)
        d['名称'] = i.get('sick_name', '')  # str
        d['多发人群'] = ''.join(i.get('多发人群', '暂无数据'))  # str
        crx = list(i.get('是否传染', ''))
        if crx == ["无传染性"]:
            d['传染性'] = False
        else:
            d['传染性'] = True
        d['症状'] = i.get('相关症状', '暂无数据').split('、')  # list
        d['治疗费用'] = ''.join(i.get('治疗费用', '暂无数据'))  # str
        d['部位'] = list(i.get('发病部位', ['暂无数据']))  # list
        d['药品'] = ''.join(i.get('相关药品', ['暂无数据'])).split('、')  # list
        d['治疗方法'] = i.get('治疗方法', '暂无数据').split('、')  # list
        d['检查项目'] = i.get('相关检查', '暂无数据').split('、')  # list
        d['疾病'] = []
        xgjb = list(i.get('相关疾病', ['暂无数据']))  # list
        for jb in xgjb:
            jb = jb.split(' ')[0]
            if jb not in d['疾病']:
                d['疾病'].append(jb)
        if d not in L:
            L.append(d)

    jsyljb = json.dumps(L, ensure_ascii=False)

    with open('yljb_new.json', 'wb') as ff:
        ff.write(jsyljb.encode('utf-8'))

    with open('yljb_new.json', 'r', encoding='utf-8') as f:  # 需要手动去除\\,和F(ab')
        content = f.read()
        l4 = json.loads(content)
        print(len(l4))
        print(l4[5])


# yl_jb()


def fh_zz():
    L=[]
    with open('飞华症状.json', 'r',encoding='utf-8') as f:
        contents = f.read()
        l = json.loads(contents)
        # print(len(l))
        # print(l[14]['易发人群'])

    for i in l:
        d={}
        d['名称'] = i.get('症状名称', '')  # str
        d['图片'] = i.get('image_link', '暂无数据')  # str
        d['科室'] = i.get('科室', ['暂无数据'])  # list
        d['部位'] = list(i.get('发病部位', ['暂无数据']))  # list
        d['定义'] = i.get('简介', '暂无数据').replace('    ', '').replace('\'', ' ')   # str
        d['检查项目'] = i.get('检查项目', ['暂无数据'])  # list
        dfrq = i.get('易发人群',None)
        if dfrq:
            d['多发人群']=dfrq
        else:
            d['多发人群'] ='暂无数据'
        d['相似症状'] = i.get('有哪些相似症状', ['暂无数据'])  # list
        d['伴随症状'] = i.get('有哪些伴随症状', ['暂无数据'])  # list

        if d not in L:
            L.append(d)

    jsfhzz = json.dumps(L, ensure_ascii=False)

    with open('fhzz_new.json', 'wb') as ff:
        ff.write(jsfhzz.encode('utf-8'))

    with open('fhzz_new.json', 'r', encoding='utf-8') as f:  # 需要手动去除\\,和F(ab')
        content = f.read()
        l4 = json.loads(content)
        print(len(l4))
        print(l4[5])
        print(l[14]['易发人群'])

# fh_zz()

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

def yljb_import():
    with open('yljb_new.json', 'r', encoding='utf-8') as f:
        content = f.read()
        l = json.loads(content)
    for b in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="疾病", property_key="名称", property_value=b['名称'])
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n:有来" % (b['名称'])
            graph.run(sql)
            if a.get('治疗费用','暂无数据')=='暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.治疗费用='%s'" % (b['名称'], b['治疗费用'])
                graph.run(sql)
            if a.get('多发人群','暂无数据')=='暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.多发人群='%s'" % (b['名称'], b['多发人群'])
                graph.run(sql)
            if a.get('传染性','暂无数据')=='暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.传染性=%s" % (b['名称'], b['传染性'])
                graph.run(sql)
        else:  # 如果不存在该疾病节点，则新建节点
            # 创建疾病节点
            node_jb = Node('疾病', '有来', 治疗费用=b['治疗费用'], 多发人群=b['多发人群'],名称=b['名称'], 传染性=b['传染性'])
            graph.merge(node_jb)

        # 更新科室
        for ks in b['科室']:
            if ks != '暂无数据':
                sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
                m = graph.run(sql).data()
                if m:  # 存在这个科室的节点
                    sql = "MATCH (n:`科室`{名称:'%s'}) set n:有来" % (ks)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_ks = Node('科室', '有来', 名称=ks)
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
                    sql = "MATCH (n:`部位`{名称:'%s'}) set n:有来" % (bw)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_bw = Node('部位', '有来', 名称=bw)
                    graph.merge(node_bw)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '部位', b['名称'], bw, '部位', '部位')
                graph.run(query)

        # 更新治疗方法
        for zl in b['治疗方法']:
            if zl != '暂无数据':
                sql = "MATCH (n:`治疗方法`{名称:'%s'}) RETURN n.名称" % (zl)
                m = graph.run(sql).data()
                if m:  # 存在这个部位的节点
                    sql = "MATCH (n:`治疗方法`{名称:'%s'}) set n:有来" % (zl)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_zl = Node('治疗方法', '有来', 名称=zl)
                    graph.merge(node_zl)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '治疗方法', b['名称'], zl, '治疗方法', '治疗方法')
                graph.run(query)

        # 更新症状
        for zz in b['症状']:
            if zz != '暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称" % (zz)
                m = graph.run(sql).data()
                if m:  # 存在症状的节点
                    sql = "MATCH (n:`症状`{名称:'%s'}) set n:有来" % (zz)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_zz = Node('症状', '有来', 名称=zz)
                    graph.merge(node_zz)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '症状', b['名称'], zz, '症状', '症状')
                graph.run(query)

        # 更新检查项目
        for jc in b['检查项目']:
            if jc != '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) RETURN n.名称" % (jc)
                m = graph.run(sql).data()
                if m:  # 存在检查项目的节点
                    sql = "MATCH (n:`检查项目`{名称:'%s'}) set n:有来" % (jc)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_jc = Node('检查项目', '有来', 名称=jc)
                    graph.merge(node_jc)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '检查项目', b['名称'], jc, '检查项目', '检查项目')
                graph.run(query)

        # 更新药品
        for yp in b['药品']:
            if yp != '暂无数据':
                sql = "MATCH (n:`药品`{名称:'%s'}) RETURN n.名称" % (yp)
                m = graph.run(sql).data()
                if m:  # 存在节点
                    sql = "MATCH (n:`药品`{名称:'%s'}) set n:有来" % (yp)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_yp = Node('药品', '有来', 名称=yp)
                    graph.merge(node_yp)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '药品', b['名称'], yp, '药品', '药品')
                graph.run(query)


yljb_import()

def fhzz_import():
    with open('fhzz_new.json', 'r', encoding='utf-8') as f:
        content = f.read()
        l = json.loads(content)
    for z in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="症状", property_key="名称", property_value=z['名称'])
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`症状`{名称:'%s'}) set n:飞华" % (z['名称'])
            graph.run(sql)
            if a.get('定义','暂无数据')=='暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) set n.定义='%s'" % (z['名称'], z['定义'])
                graph.run(sql)
            if a.get('多发人群','暂无数据')=='暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) set n.多发人群='%s'" % (z['名称'], z['多发人群'])
                graph.run(sql)
            if a.get('图片','暂无数据')=='暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) set n.图片='%s'" % (z['名称'], z['图片'])
                graph.run(sql)
        else:  # 如果不存在该疾病节点，则新建节点
            # 创建疾病节点
            node_zz = Node('症状', '飞华', 定义=z['定义'], 名称=z['名称'], 多发人群=z['多发人群'], 图片=z['图片'])
            graph.merge(node_zz)

        # 更新科室
        for ks in z['科室']:
            if ks != '暂无数据':
                sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
                m = graph.run(sql).data()
                if m:  # 存在这个科室的节点
                    sql = "MATCH (n:`科室`{名称:'%s'}) set n:飞华" % (ks)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_ks = Node('科室', '飞华', 名称=ks)
                    graph.merge(node_ks)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '科室', z['名称'], ks, '科室', '科室')
                graph.run(query)

        # 更新部位
        for bw in z['部位']:
        # bw = z.get('部位','暂无数据')
            if bw != '暂无数据':
                sql = "MATCH (n:`部位`{名称:'%s'}) RETURN n.名称" % (bw)
                m = graph.run(sql).data()
                if m:  # 存在这个部位的节点
                    sql = "MATCH (n:`部位`{名称:'%s'}) set n:飞华" % (bw)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_bw = Node('部位', '飞华', 名称=bw)
                    graph.merge(node_bw)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '部位', z['名称'], bw, '部位', '部位')
                graph.run(query)

        # 更新疾病
        # for jb in z['疾病']:
        #     if jb != '暂无数据':
        #         sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (jb)
        #         m = graph.run(sql).data()
        #         if m:  # 存在症状的节点
        #             sql = "MATCH (n:`疾病`{名称:'%s'}) set n:全民健康" % (jb)
        #             graph.run(sql)
        #         else:  # 不存在该节点
        #             node_jb = Node('疾病', '全民健康', 名称=jb)
        #             graph.merge(node_jb)
        #         query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #             '疾病', '症状', jb ,z['名称'], '症状', '症状')
        #         graph.run(query)

        # 更新检查项目
        for jc in z['检查项目']:
            if jc != '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) RETURN n.名称" % (jc)
                m = graph.run(sql).data()
                if m:  # 存在检查项目的节点
                    sql = "MATCH (n:`检查项目`{名称:'%s'}) set n:飞华" % (jc)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_jc = Node('检查项目', '飞华', 名称=jc)
                    graph.merge(node_jc)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '检查项目', z['名称'], jc, '检查项目', '检查项目')
                graph.run(query)

    # 更新相似症状
    for z in l:
        for zz in z['相似症状']:
            if zz != '暂无数据':
                sql = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称" % (zz)
                m = graph.run(sql).data()
                if m:  # 存在症状的节点
                    sql = "MATCH (n:`症状`{名称:'%s'}) set n:飞华" % (zz)
                    graph.run(sql)
                else:  # 不存在该节点
                    node_zz = Node('症状', '飞华', 名称=zz)
                    graph.merge(node_zz)
                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '症状', z['名称'], zz, '相似症状', '相似症状')
                graph.run(query)


fhzz_import()