from py2neo import Graph,Node
import json

# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123")
graph = Graph(
            host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password = "m4eeee")

with open('../prepare_data/xywy_jc_1.json','r',encoding='utf-8') as file:
    content = file.read()
    content = json.loads(content)   #[{},{},{}]
    print(type(content))
    print(len(content))

    for dict in content:
        a = graph.find_one(label="检查项目", property_key="名称", property_value=dict['名称'].strip())
        print(a)
        if a:  # 如果不为none,则更新
            # 更新标签
            sql = "MATCH (n:`检查项目`{名称:'%s'}) set n:寻医问药" % (dict['名称'].replace('\\','\\\\'))
            graph.run(sql)
            if a.get('注意事项', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.注意事项='%s'" % (dict['名称'], dict['注意事项'])
                graph.run(sql)
            # if a.get('相关检查', ['暂无数据']) == ['暂无数据']:
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.相关检查='%s'" % (dict['名称'], dict['病因'])
            #     graph.run(sql)
            # if a.get('相关检查', ['暂无数据']) != ['暂无数据']:
            #     xgjc = list(set(dict['相关检查']+a.get('相关检查')))
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.相关检查='%s'" % (dict['名称'], xgjc)
            #     graph.run(sql)
            # if a.get('科室', ['暂无数据']) == ['暂无数据']:
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.科室='%s'" % (dict['名称'], dict['病症详述'])
            #     graph.run(sql)
            # if a.get('科室', ['暂无数据']) != ['暂无数据']:
            #     ks = list(set(dict['科室']+a.get('科室')))
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.科室='%s'" % (dict['名称'], ks)
            #     graph.run(sql)


            # if a.get('相关疾病', ['暂无数据']) == ['暂无数据']:
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.相关疾病='%s'" % (dict['名称'], dict['相关疾病'])
            #     print(sql)
            #     graph.run(sql)
            #
            # if a.get('相关疾病', ['暂无数据']) != ['暂无数据']:
            #     xgjb = list(set(a.get('相关疾病')+dict['相关疾病']))
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.相关疾病='%s'" % (dict['名称'], xgjb)
            #     print(sql)
            #     graph.run(sql)

            if a.get('检查过程', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.检查过程='%s'" % (dict['名称'].replace('\\','\\\\'), dict['检查过程'])
                print(sql)
                graph.run(sql)
            if a.get('参考价格', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.参考价格='%s'" % (dict['名称'].replace('\\','\\\\'), dict['参考价格'])
                print(sql)
                graph.run(sql)
            if a.get('适用性别', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.适用性别='%s'" % (dict['名称'].replace('\\','\\\\'), dict['适用性别'])
                print(sql)
                graph.run(sql)


            if a.get('是否空腹', '暂无数据') == '暂无数据':
                print(a.get('是否空腹'))
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.是否空腹='%s'" % (dict['名称'].replace('\\','\\\\'), dict.get('是否空腹',''))
                print(sql)
                graph.run(sql)
            # if a.get('是否空腹','暂无数据') != dict.get('是否空腹'):
            #     print(a.get('是否空腹'))
            #     sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.是否空腹='%s'" % (dict['名称'].replace('\\','\\\\'), '争议')
            #     print(sql)
            #     graph.run(sql)

            if a.get('检查分类', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.检查分类='%s'" % (dict['名称'].replace('\\','\\\\'), dict['检查分类'])
                print(sql)
                graph.run(sql)

            if a.get('不适宜人群', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.不适宜人群='%s'" % (dict['名称'].replace('\\','\\\\'), dict['不适宜人群'])
                print(sql)
                graph.run(sql)

            if a.get('检查项目简介', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.检查项目简介='%s'" % (dict['名称'].replace('\\','\\\\'), dict['检查项目简介'])
                print(sql)
                graph.run(sql)

            if a.get('不良反应与风险', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.不良反应与风险='%s'" % (dict['名称'].replace('\\','\\\\'), dict['不良反应与风险'])
                print(sql)
                graph.run(sql)

            if a.get('临床意义', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.临床意义='%s'" % (dict['名称'].replace('\\','\\\\'), dict['临床意义'])
                print(sql)
                graph.run(sql)

            if a.get('温馨提示', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.温馨提示='%s'" % (dict['名称'].replace('\\','\\\\'), dict['温馨提示'])
                print(sql)
                graph.run(sql)

            if a.get('正常值', '暂无数据') == '暂无数据':
                sql = "MATCH (n:`检查项目`{名称:'%s'}) set n.正常值='%s'" % (dict['名称'].replace('\\','\\\\'), dict['正常值'])
                print(sql)
                graph.run(sql)


        else:  # 如果不存在该检查项目节点，则新建节点
            # 创建检查项目节点
            node_jdict = Node('检查项目', '寻医问药', 名称=dict['名称'], 注意事项=dict['注意事项'],
                              检查过程=dict['检查过程'],参考价格=dict['参考价格'],适用性别=dict['适用性别'],是否空腹=dict.get('是否空腹'),
                              检查分类=dict['检查分类'],不适宜人群=dict['不适宜人群'],检查项目简介=dict['检查项目简介'],
                              不良反应与风险=dict['不良反应与风险'],临床意义=dict['临床意义'],温馨提示=dict['温馨提示'],正常值=dict['正常值'])
            graph.merge(node_jdict)


        # 更新相关症状
        for xgzz in dict.get('相关症状',['暂无数据']):
            if xgzz != ['暂无数据']:
                cql = """match (n:症状) where n.名称='%s' return n"""%xgzz
                m = graph.run(cql)
                if m:
                    cql = """ match (n:症状) where n.名称='%s' set n:寻医问药"""%xgzz
                else:
                    node_jc = Node('症状','寻医问药',名称=xgzz)
                    graph.merge(node_jc)

                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '症状', '检查项目', xgzz, dict['名称'].replace('\\','\\\\'),  '检查项目', '检查项目')
                graph.run(query)

        # 更新相关疾病
        for xgjb in dict.get('相关疾病',['暂无数据']):
            if xgjb != ['暂无数据']:
                cql = """match (n:疾病) where n.名称='%s' return n"""%xgjb
                m = graph.run(cql)
                if m:
                    cql = """ match (n:疾病) where n.名称='%s' set n:寻医问药"""%xgjb
                else:
                    node_jc = Node('疾病','寻医问药',名称=xgjb)
                    graph.merge(node_jc)

                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                    '疾病', '检查项目', xgjb, dict['名称'].replace('\\','\\\\'),'检查项目', '检查项目')
                graph.run(query)

        # 更新科室

        for ks in dict.get('科室',['暂无数据']):
            if ks != ['暂无数据']:
                cql = """match (n:科室) where n.名称= '%s' return n"""%ks
                m = graph.run(cql)
                if m:
                    cql = """ match (n:科室) where n.名称='%s' set n:寻医问药"""%ks
                else:
                    node_jc = Node('科室','寻医问药',名称=ks)
                    graph.merge(node_jc)

                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)<-[rel:%s{名称:'%s'}]-(q)" % (
                    '科室', '检查项目', ks, dict['名称'].replace('\\','\\\\'), '科室', '科室')
                graph.run(query)

        # 更新检查项目

        for jcxm in dict.get('相关检查',['暂无数据']):
            if jcxm != ['暂无数据']:
                cql = """match (n:检查项目) where n.名称='%s' return n"""%jcxm.replace('\\','\\\\')
                m = graph.run(cql)
                if m:
                    cql = """ match (n:检查项目) where n.名称='%s' set n:寻医问药"""%jcxm.replace('\\','\\\\')
                else:
                    node_jc = Node('检查项目','寻医问药',名称=jcxm)
                    graph.merge(node_jc)

                query = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)<-[rel:%s{名称:'%s'}]-(q)" % (
                    '检查项目', '检查项目', jcxm.replace('\\','\\\\'), dict['名称'], '相关检查', '相关检查')
                graph.run(query)


