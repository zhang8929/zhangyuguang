"""39 网站检查项目入库"""
from py2neo import Graph,Node
import json


graph = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123")
# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password = "m4eeee")

def import_39jiancha():
    with open('../prepare_data/39_检查.json','r',encoding='utf-8') as file:
        content = file.read()
        content = json.loads(content)
        print(len(content))
        print(len(content[4].keys()))
        print(content[6].keys())
        print(content[4].keys())

        for dict in content:
            name = dict.get('名称')
            if '\\' in name:
                name = name.replace('\\', '\\\\')

            cql = """match (n:检查项目) where n.名称='%s' return n"""%name
            res = graph.run(cql)
            if res:
                cql = """match (n:检查项目) where n.名称='%s' set n:三九"""%name
            else:
                node = Node('检查项目','三九',名称=dict.get('名称',''),别名=dict.get('别名',['暂无数据']),
                            检查项目简介=dict.get('检查项目简介'),)

            #更新科室，疾病，症状，部位
                # 更新相关症状
            for xgzz in dict.get('相关症状', ['暂无数据']):
                if xgzz != '暂无数据':
                    cql = """match (n:症状) where n.名称='%s' return n""" % xgzz
                    m = graph.run(cql)
                    if m:
                        cql = """ match (n:症状) where n.名称='%s' set n:三九""" % xgzz
                    else:
                        node_jc = Node('症状', '三九', 名称=xgzz)
                        graph.merge(node_jc)

                    query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                        '症状', '检查项目', xgzz, name, '检查项目', '检查项目')
                    graph.run(query)

            # 更新相关疾病
            for xgjb in dict.get('相关疾病', ['暂无数据']):
                if xgjb != '暂无数据':
                    cql = """match (n:疾病) where n.名称='%s' return n""" % xgjb
                    m = graph.run(cql)
                    if m:
                        cql = """ match (n:疾病) where n.名称='%s' set n:三九""" % xgjb
                    else:
                        node_jc = Node('疾病', '三九', 名称=xgjb)
                        graph.merge(node_jc)

                    query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                        '疾病', '检查项目', xgjb, name, '检查项目', '检查项目')
                    graph.run(query)

            # 更新科室

            for ks in dict.get('科室', ['暂无数据']):
                if ks != '暂无数据':
                    cql = """match (n:科室) where n.名称= '%s' return n""" % ks
                    m = graph.run(cql)
                    if m:
                        cql = """ match (n:科室) where n.名称='%s' set n:三九""" % ks
                    else:
                        node_jc = Node('科室', '三九', 名称=ks)
                        graph.merge(node_jc)

                    query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)<-[rel:%s{名称:'%s'}]-(q)" % (
                        '科室', '检查项目', ks, name, '科室', '科室')
                    graph.run(query)

            for bw in dict.get('检查部位_list', ['暂无数据']):
                if bw != '暂无数据':
                    cql = """match (n:科室) where n.名称= '%s' return n""" % bw
                    m = graph.run(cql)
                    if m:
                        cql = """ match (n:科室) where n.名称='%s' set n:三九""" % bw
                    else:
                        node_bw = Node('科室', '三九', 名称=bw)
                        graph.merge(node_bw)

                    query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                        '检查项目','部位',name, bw, '部位', '部位')
                    graph.run(query)
        



