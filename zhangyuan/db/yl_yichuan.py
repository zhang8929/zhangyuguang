# coding: utf-8
from py2neo import Node, Relationship, Graph
from pandas import DataFrame
import json
# import codecs
import re

graph = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123")
# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="m4eeee")


def yljb_import():
    """
    为线上图库中的疾病增加遗传性属性
    :return:
    """
    with open('yljb_new.json', 'r', encoding='utf-8') as f:
        content = f.read()
        l = json.loads(content)
    for b in l:
        # sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (b['名称'])
        # m = graph.run(sql).data()
        a = graph.find_one(label="疾病", property_key="名称", property_value=b['名称'])
        if a:  # 如果不为none,则更新
            # 更新属性
            if a.get('遗传性','暂无数据')=='暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.遗传性=%s" % (b['名称'],b['遗传性'])
                graph.run(sql)
        else:  # 如果不存在该疾病节点，则新建节点
            # 创建疾病节点
            node_jb = Node('疾病', '有来', 治疗费用=b['治疗费用'], 多发人群=b['多发人群'],名称=b['名称'], 传染性=b['传染性'], 遗传性=b['遗传性'])
            graph.merge(node_jb)
    print('导入完毕')


def sanjiu_surgery(): #手术方式和部位
    with open('./prepare_data/39_surgery.json','r',encoding='utf-8') as file:
        content = file.read()
        content= json.loads(content)

        for dict in content:
            a = graph.find_one(label='手术',property_key='名称',property_value=dict['名称'])
            if a:
                if a.get('手术方式','暂无数据'):
                    sql = """match (n:手术) where n.名称="%s" set n.手术方式="%s" """%(dict['名称'],dict.get('手术方式','暂无数据'))
                    graph.run(sql)

        #更新部位
            for bw in dict.get('手术部位：',['暂无数据']):
                print()
                if bw=='手部':
                    bw = '手'
                if bw == '面部':
                    bw = '面'
                if bw == '耳部':
                    bw = '耳'
                if bw=='足部':
                    bw = '足'
                if bw=='鼻部':
                    bw = '鼻'
                if bw=='口部':
                    bw = '口'
                if bw=='眼部':
                    bw = '眼'
                cql="""match (n:部位) where n.名称='%s' return n"""%bw
                res = graph.run(cql)
                if res:  #说明有部位
                    cql = """match (n:部位) where n.名称='%s' set n:三九"""%bw
                    print(cql)
                    graph.run(cql)
                else:
                    node_bw = Node('部位','三九',名称='%s'%bw)
                    graph.merge(node_bw)

                #创建关系
                cql = """match (n:手术),(m:部位) where n.名称='%s' and m.名称='%s' merge (n)-[rel:部位{名称:'部位'}]->(m)"""%(dict.get('名称',''),bw)
                print(cql)
                graph.run(cql)


    print('手术方式完毕')


if __name__ == '__main__':
    yljb_import()
    sanjiu_surgery()