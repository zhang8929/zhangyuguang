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
graph = Graph(
            host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="m4eeee")

with codecs.open('xywy_new2.json', 'r',encoding='utf-8') as f:
    contents = f.read()
    l = json.loads(contents)
    # print(len(l))
    # print(l[18])
    # print(l[22])


for b in l:
    # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
    # m = graph.run(sql).data()
    a = graph.find_one(label="疾病", property_key="名称", property_value=b['名称'])
    if a:  # 如果不为none,则更新
        #更新标签
        sql = "MATCH (n:`疾病`{名称:'%s'}) set n:寻医问药" % (b['名称'])
        graph.run(sql)
        #更新别称
        if b['别称']!=['暂无数据']:
            if a['别称']!=['暂无数据']:
                for bc in b['别称']:
                    if bc not in a['别称']:
                        a['别称'].append(bc)
            else:
                a['别称']=b['别称']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.别称='%s'" % (b['名称'],a['别称'])
            graph.run(sql)

        #更新英文名
        if a['英文名']=='暂无数据':
            a['英文名']=b['英文名']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.英文名='%s'" % (b['名称'], a['英文名'])
            graph.run(sql)

        #更新定义
        if a['定义']=='暂无数据':
            a['定义']=b['定义']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.定义='%s'" % (b['名称'], a['定义'])
            graph.run(sql)

        # 更新病因，均有数据则不更新
        if a['病因']=='暂无数据':
            a['病因']=b['病因']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.病因='%s'" % (b['名称'], a['病因'])
            graph.run(sql)
        # 更新多发人群，均有数据则不更新
        if a['多发人群']=='暂无数据':
            a['多发人群']=b['多发人群']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.多发人群='%s'" % (b['名称'], a['多发人群'])
            graph.run(sql)
        # 更新治疗费用
        if a['治疗费用'] == '暂无数据':
            a['治疗费用'] = b['治疗费用']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.治疗费用='%s'" % (b['名称'], a['治疗费用'])
            graph.run(sql)
        #更新患病比例值
        if a['患病比例值'] == -1:
            a['患病比例值'] = b['患病比例值']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.患病比例值='%s'" % (b['名称'], a['患病比例值'])
            graph.run(sql)
        #更新治愈率值
        if a['治愈率值'] == -1:
            a['治愈率值'] = b['治愈率值']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.治愈率值='%s'" % (b['名称'], a['治愈率值'])
            graph.run(sql)
        #更新温馨提示
        if a['温馨提示'] == '暂无数据':
            a['温馨提示'] = b['温馨提示']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.温馨提示='%s'" % (b['名称'], a['温馨提示'])
            graph.run(sql)
        #更新治疗周期
        if a['治疗周期'] == '暂无数据':
            a['治疗周期'] = b['治疗周期']
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n.治疗周期='%s'" % (b['名称'], a['治疗周期'])
            graph.run(sql)
        # 医保/传染性暂不更新

    else:  # 如果不存在该疾病节点，则新建节点
        # 创建疾病节点
        node_jb = Node('疾病', '寻医问药', 病因=b['病因'], 别称=b['别称'], 英文名=b['英文名'], 温馨提示=b['温馨提示'], 患病比例=b['患病比例'],
                       定义=b['定义'], 名称=b['名称'], 治疗费用=b['治疗费用'], 多发人群=b['多发人群'], 患病比例值=b['患病比例值'],
                       医保=b['医保'], 传染性=b['传染性'], 治疗周期=b['治疗周期'], 治愈率=b['治愈率'], 治愈率值=b['治愈率值'])
        graph.merge(node_jb)

    #更新科室
    for ks in b['科室']:
        if ks!='暂无数据':
            sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (ks)
            m = graph.run(sql).data()
            if m:#存在这个科室的节点
                sql = "MATCH (n:`科室`{名称:'%s'}) set n:寻医问药" % (ks)
                graph.run(sql)
            else:#不存在该节点
                node_ks = Node('科室','寻医问药', 名称=ks)
                graph.merge(node_ks)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '科室', b['名称'], ks, '科室','科室')
            graph.run(query)

    #更新部位,暂无数据不更新

    #更新症状
    for zz in b['症状']:
        if zz != '暂无数据':
            sql = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称" % (zz)
            m = graph.run(sql).data()
            if m: # 存在症状的节点
                sql = "MATCH (n:`症状`{名称:'%s'}) set n:寻医问药" % (zz)
                graph.run(sql)
            else:  # 不存在该节点
                node_zz = Node('症状','寻医问药', 名称=zz)
                graph.merge(node_zz)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '症状', b['名称'], zz, '症状', '症状')
            graph.run(query)

    #更新检查项目
    for jc in b['检查项目']:
        if jc != '暂无数据':
            sql = "MATCH (n:`检查项目`{名称:'%s'}) RETURN n.名称" % (jc)
            m = graph.run(sql).data()
            if m:  # 存在检查项目的节点
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n:寻医问药" % (jc)
                graph.run(sql)
            else:  # 不存在该节点
                node_jc = Node('检查项目','寻医问药', 名称=jc)
                graph.merge(node_jc)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '检查项目', b['名称'], jc, '检查项目', '检查项目')
            graph.run(query)

    #更新治疗方法
    for zl in b['治疗方法']:
        if zl != '暂无数据':
            sql = "MATCH (n:`治疗方法`{名称:'%s'}) RETURN n.名称" % (zl)
            m = graph.run(sql).data()
            if m:  # 存在治疗方法的节点
                sql = "MATCH (n:`治疗方法`{名称:'%s'}) set n:寻医问药" % (zl)
                graph.run(sql)
            else:  # 不存在该节点
                node_zl = Node('治疗方法','寻医问药', 名称=zl)
                graph.merge(node_zl)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '治疗方法', b['名称'], zl, '治疗方法', '治疗方法')
            graph.run(query)

    # 更新药品
    for yp in b['药品']:
        if yp != '暂无数据':
            sql = "MATCH (n:`药品`{名称:'%s'}) RETURN n.名称" % (yp)
            m = graph.run(sql).data()
            if m:  # 存在节点
                sql = "MATCH (n:`药品`{名称:'%s'}) set n:寻医问药" % (yp)
                graph.run(sql)
            else:  # 不存在该节点
                node_yp = Node('药品', '寻医问药', 名称=yp)
                graph.merge(node_yp)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '药品', b['名称'], yp, '药品', '药品')
            graph.run(query)


    # 更新传播途径
    for cb in b['传播途径']:
        if cb != '暂无数据' and cb != '无':
            sql = "MATCH (n:`传播途径`{名称:'%s'}) RETURN n.名称" % (cb)
            m = graph.run(sql).data()
            if m:  # 存在节点
                sql = "MATCH (n:`传播途径`{名称:'%s'}) set n:寻医问药" % (cb)
                graph.run(sql)
            else:  # 不存在该节点
                node_cb = Node('传播途径', '寻医问药', 名称=cb)
                graph.merge(node_cb)
            query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '传播途径', b['名称'], cb, '传播途径', '传播途径')
            graph.run(query)

#更新并发疾病
for b in l:
    # 创建并发疾病关系
    for jb in b['并发疾病']:
        if jb != '暂无数据':
            query8 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                '疾病', '疾病', b['名称'], jb, '并发疾病', '并发疾病')
            graph.run(query8)


        # 更新科室
        # for k in b['科室']:
        #     if k != '暂无数据':
        #         sql = "MATCH (n:`科室`{名称:'%s'}) RETURN n.名称" % (k)
        #         m = graph.run(sql).data()
        #         if m:  # 存在这个科室的节点
        #             sql = "MATCH (n:`科室`{名称:'%s'}) set n:寻医问药" % (k)
        #             graph.run(sql)
        #         else:  # 不存在该节点
        #             node_ks = Node('科室', '寻医问药', 名称=k)
        #             graph.merge(node_ks)
        #         query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #             '疾病', '科室', b['名称'], k, '科室', '科室')
        #         graph.run(query)

        # 更新部位,暂无数据不更新

        # 更新症状
        # for zz in b['症状']:
        #     if zz != '暂无数据':
        #         sql = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称" % (zz)
        #         m = graph.run(sql).data()
        #         if m:  # 存在症状的节点
        #             sql = "MATCH (n:`症状`{名称:'%s'}) set n:寻医问药" % (zz)
        #             graph.run(sql)
        #         else:  # 不存在该节点
        #             node_zz = Node('症状', '寻医问药', 名称=zz)
        #             graph.merge(node_zz)
        #         query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #             '疾病', '症状', b['名称'], zz, '症状', '症状')
        #         graph.run(query)

        # 更新检查项目
        # for jc in b['检查项目']:
        #     if jc != '暂无数据':
        #         sql = "MATCH (n:`检查项目`{名称:'%s'}) RETURN n.名称" % (jc)
        #         m = graph.run(sql).data()
        #         if m:  # 存在检查项目的节点
        #             sql = "MATCH (n:`检查项目`{名称:'%s'}) set n:寻医问药" % (jc)
        #             graph.run(sql)
        #         else:  # 不存在该节点
        #             node_jc = Node('检查项目', '寻医问药', 名称=jc)
        #             graph.merge(node_jc)
        #         query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #             '疾病', '检查项目', b['名称'], jc, '检查项目', '检查项目')
        #         graph.run(query)

        # 更新治疗方法
        # for zl in b['治疗方法']:
        #     if zl != '暂无数据':
        #         sql = "MATCH (n:`治疗方法`{名称:'%s'}) RETURN n.名称" % (zl)
        #         m = graph.run(sql).data()
        #         if m:  # 存在治疗方法的节点
        #             sql = "MATCH (n:`治疗方法`{名称:'%s'}) set n:寻医问药" % (zl)
        #             graph.run(sql)
        #         else:  # 不存在该节点
        #             node_zl = Node('治疗方法', '寻医问药', 名称=zl)
        #             graph.merge(node_zl)
        #         query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #             '疾病', '治疗方法', b['名称'], zl, '治疗方法', '治疗方法')
        #         graph.run(query)

        # 更新药品
        # for yp in b['药品']:
        #     if yp != '暂无数据':
        #         sql = "MATCH (n:`药品`{名称:'%s'}) RETURN n.名称" % (yp)
        #         m = graph.run(sql).data()
        #         if m:  # 存在节点
        #             sql = "MATCH (n:`药品`{名称:'%s'}) set n:寻医问药" % (yp)
        #             graph.run(sql)
        #         else:  # 不存在该节点
        #             node_yp = Node('药品', '寻医问药', 名称=yp)
        #             graph.merge(node_yp)
        #         query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
        #             '疾病', '药品', b['名称'], yp, '药品', '药品')
        #         graph.run(query)

