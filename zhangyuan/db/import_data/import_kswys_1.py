from py2neo import Graph,Node
import json

# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123")
# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password = "m4eeee")

with open('../prepare_data/kswys_1.json','r',encoding='utf-8') as file:
    content = file.read()
    content = json.loads(content)   #[{},{},{}]
    print(type(content))
    print(len(content))

    for dict in content:
        a = graph.find_one(label="疾病", property_key="名称", property_value=dict['名称'])
        print(a)
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`疾病`{名称:'%s'}) set n:快速问医生" % (dict['名称'])
            graph.run(sql)
            if a.get('饮食保健', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.饮食保健='%s'" % (dict['名称'], dict['饮食保健'])
                graph.run(sql)
            if a.get('病因', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.病因='%s'" % (dict['名称'], dict['病因'])
                graph.run(sql)
            if a.get('病症详述', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.病症详述='%s'" % (dict['名称'], dict['病症详述'])
                graph.run(sql)
            if a.get('检查内容详述', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.检查内容详述='%s'" % (dict['名称'], dict['检查内容详述'])
                print(sql)
                graph.run(sql)
            if a.get('鉴别详述', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.鉴别详述='%s'" % (dict['名称'], dict['鉴别详述'])
                print(sql)
                graph.run(sql)
            if a.get('预防详述', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.预防详述='%s'" % (dict['名称'], dict['预防详述'])
                print(sql)
                graph.run(sql)
            if a.get('治疗方法详述', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.治疗方法详述='%s'" % (dict['名称'], dict['治疗方法详述'])
                print(sql)
                graph.run(sql)
            if a.get('宜吃', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.宜吃='%s'" % (dict['名称'], dict['宜吃'])
                print(sql)
                graph.run(sql)
            if a.get('忌吃', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`疾病`{名称:'%s'}) set n.忌吃='%s'" % (dict['名称'], dict['忌吃'])
                print(sql)
                graph.run(sql)

        else:  # 如果不存在该疾病节点，则新建节点
            # 创建疾病节点
            node_jdict = Node('疾病', '快速问医生', 饮食保健=dict['饮食保健'], 病因=dict['病因'], 病症详述=dict['病症详述'],
                              检查内容详述=dict['检查内容详述'],鉴别详述=dict['鉴别详述'],预防详述=dict['预防详述'],
                              治疗方法详述=dict['治疗方法详述'],宜吃=dict['宜吃'],忌吃=dict['忌吃'])
            graph.merge(node_jdict)


        for jc in dict.get('检查项目','暂无数据'):
            if jc != '暂无数据':
                cql = """match (n:检查项目) where n.名称='%s' return n"""%jc
                m = graph.run(cql)
                if m:
                    cql = """ match (n:检查项目) where n.名称='%s' set n:快速问医生"""%jc
                else:
                    node_jc = Node('检查项目','快速问医生',名称=jc)
                    graph.merge(node_jc)

                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '检查项目', dict['名称'], jc, '检查项目', '检查项目')
                graph.run(query)
