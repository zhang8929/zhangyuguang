import json
from py2neo import Graph,Node

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


def import_39surgery():
    with open('../prepare_data/39_surgery.json','r',encoding='utf-8') as file:
        content = file.read()
        content = json.loads(content)
        print(len(content))
        print(len(content[4].keys()))
        print(content[6].keys())
        print(content[4].keys())


        # for i in range(len(content)-1):
        #     print(len(content[i]))


        for dict in content:
            name = dict.get('名称')
            # 创建节点
            node_ss = Node('手术','三九',名称=dict.get('名称','暂无数据'),麻醉方式=dict.get('麻醉方式','暂无数据'),
                           手术简介=dict.get('手术简介', '暂无数据'),手术部位=dict.get('手术部位','暂无数据'),
                           医保=dict.get('医保', ''),
                           手术过程=dict.get('手术过程','暂无数据'),别名=dict.get('别名',['暂无数据']),
                           手术适应症=dict.get('手术适应症','暂无数据'),不适宜人群=dict.get('不适宜人群','暂无数据'),
                           手术时间=dict.get('手术时间','暂无数据'),手术术后=dict.get('手术术后','暂无数据'),
                           术前准备=dict.get('术前准备','暂无数据'),分类=dict.get('分类','暂无数据'),
                           )


            # 关系创建--对每一个手术创建与疾病，科室，症状之间的关系
            # 相关疾病
            print('----')

            print(type(dict.get('相关疾病',['暂无数据'])))
            n=0
            for jb in dict.get('相关疾病',['暂无数据']):
                if jb != '暂无数据':
                    print(jb)
                    cql = """match (n:疾病) where n.名称='%s' return n """%jb
                    res = graph.run(cql)
                    if res:#有此疾病节点
                        cql = """match (n:疾病) where n.名称='%s' set n:三九"""
                    else:
                        node_jb = Node('疾病','三九',名称='%s'%jb)
                        n+=1
                        graph.merge(node_jb)

                    cql = """match (n:疾病),(m:手术) where n.名称='%s' and m.名称='%s' merge (n)-[rel:手术{名称:'手术'}]->(m) """%(jb,dict.get('名称',''))
                    print(cql)
                    graph.run(cql)


            # 相关症状
            for zz in dict.get('相关症状', ['暂无数据']):
                if zz != '暂无数据':
                    cql = """match (n:症状) where n.名称='%s' return n """ % zz
                    res = graph.run(cql)
                    if res:  # 有此症状节点
                        cql = """match (n:症状) where n.名称='%s' set n:三九"""%zz
                    else:
                        node_jb = Node('症状', '三九', 名称='%s' % zz)
                        graph.merge(node_jb)

                    cql = """match (n:症状),(m:手术) where n.名称='%s' and m.名称='%s' merge (n)-[rel:手术{名称:'手术'}]->(m) """%(zz,dict.get('名称',''))
                    graph.run(cql)

            # 科室
            for ks in dict.get('科室',['暂无数据']):
                if ks != '暂无数据':
                    cql = """match (n:科室) where n.名称='%s' return n"""%ks
                    res = graph.run(cql)
                    if res:
                        cql = """match (n:科室) where n.名称='%s' set n:三九"""%ks
                    else:
                        node_ks = Node('科室','三九',名称='%s'%ks)

                    cql = """match (n:科室), (m:手术) where n.名称='%s' and m.名称='%s' merge (n)<-[rel:所属科室{名称:'所属科室'}]-(m)"""%(ks,dict.get('名称',''))
                    graph.run(cql)


if __name__ == '__main__':
    import_39surgery()