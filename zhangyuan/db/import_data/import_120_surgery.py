from py2neo import Graph,Node
import json

'''导入120 手术数据'''
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


with open('../../爬虫数据/120/手术120.json','r',encoding='utf-8') as file:
    content = file.read()

    print(type(content))
    content = json.loads(content)

    for dict in content:
        name = dict.get('手术名称').replace('"',"'")
        if '\\' in name:
            name = name.replace('\\','\\\\')
        neo_node = graph.find_one(label="手术", property_key="名称", property_value=name)
        if neo_node:
            cql = """match (n:手术) where n.名称="%s" set n:快速问医生 """%name
            graph.run(cql)

            sqzb = neo_node.get('术前准备', '暂无数据')
            if sqzb == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.术前准备="%s" """ % (name, dict.get('术前准备', '暂无数据').replace('\\','\\\\').replace('"',"'").strip())
                print(sql)
                graph.run(sql)

            jg = neo_node.get('手术费用', '暂无数据')
            if jg == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术费用="%s" """ % (
                name, dict.get('手术报价', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            mz = neo_node.get('麻醉方式', '暂无数据')
            if mz == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.麻醉方式="%s" """ % (
                    name, dict.get('麻醉方式', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            ssfs = neo_node.get('手术方式', '暂无数据')
            if ssfs == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术方式="%s" """ % (
                    name, dict.get('手术方式', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            sssyz = neo_node.get('手术适应症', '暂无数据')
            if sssyz == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术适应症="%s" """ % (
                    name, dict.get('适应症', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            sqzb = neo_node.get('注意事项', '暂无数据')
            if sqzb == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.术前准备="%s" """ % (
                    name, dict.get('术前准备', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            ssgc = neo_node.get('手术过程', '暂无数据')
            if sqzb == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术过程="%s" """ % (
                    name, dict.get('手术步骤', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            sssh = neo_node.get('手术术后', '暂无数据')
            if sqzb == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术术后="%s" """ % (
                    name, dict.get('术后护理', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            sqzb = neo_node.get('手术禁忌', '暂无数据')
            if sqzb == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术禁忌="%s" """ % (
                    name, dict.get('手术禁忌', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)

            ssbfz = neo_node.get('并发症', '暂无数据')
            if ssbfz == '暂无数据':
                sql = """match (n:手术) where n.名称="%s" set n.手术并发症="%s" """ % (
                    name, dict.get('并发症', '暂无数据').replace('\\', '\\\\').replace('"', "'").strip())
                print(sql)
                graph.run(sql)


        else:
            node_ss = Node('手术','快速问医生',名称=name, 术前准备=dict.get('术前准备','暂无数据'),
                           手术费用=dict.get('手术报价','暂无数据'),麻醉方式=dict.get('麻醉','暂无数据'),
                           手术方式=dict.get('手术方式','暂无数据'),手术适应症=dict.get('适应症','暂无数据'),
                           手术术前=dict.get('注意事项','暂无数据'),手术过程=dict.get('手术步骤','暂无数据'),
                           手术术后=dict.get('术后护理','暂无数据'),并发症=dict.get('并发症','暂无数据'),
                           手术禁忌=dict.get('手术禁忌','暂无数据')
                           )
            graph.merge(node_ss)


        # 更新部位
        ssbw = dict.get('部位',['暂无数据'])
        for bw in ssbw:
            if bw != '暂无数据':

                cql = """match (n:部位) where n.名称="%s" return n """ % bw.replace('\\', '\\\\').replace('"', "'")
                res = graph.run(cql)
                if res:  # 有此部位节点
                    cql = """match (n:部位) where n.名称="%s" set n:快速问医生""" % bw.replace('\\', '\\\\').replace('"', "'")
                    graph.run(cql)
                else:
                    node_jb = Node('部位', '快速问医生', 名称='%s' % bw)
                    graph.merge(node_jb)

                cql = """match (n:部位),(m:手术) where n.名称="%s" and m.名称="%s" merge (n)<-[rel:部位{名称:'部位'}]-(m) """ % (
                bw.replace('\\', '\\\\').replace('"', "'"), name)
                print(cql)
                graph.run(cql)


        # 更新科室
        ssks = dict.get('科室','暂无数据')
        if ssks is None:
            ssks = "暂无数据"
        ssks = ssks.split()
        for ks in ssks:
            if ks != '暂无数据':
                cql = """match (n:科室) where n.名称='%s' return n """ % bw.replace('\\', '\\\\').replace('"', "'")
                res = graph.run(cql)
                if res:  # 有此部位节点
                    cql = """match (n:科室) where n.名称='%s' set n:快速问医生""" % bw.replace('\\', '\\\\').replace('"', "'")
                    graph.run(cql)
                else:
                    node_jb = Node('科室', '快速问医生', 名称='%s' % ks)
                    graph.merge(node_jb)

                cql = """match (n:科室),(m:手术) where n.名称="%s" and m.名称="%s" merge (n)<-[rel:所属科室{名称:'所属科室'}]-(m) """ % (
                    ks.replace('\\', '\\\\').replace('"', "'"), name)
                print(cql)
                graph.run(cql)





