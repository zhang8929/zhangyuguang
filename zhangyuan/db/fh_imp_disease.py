from py2neo import Graph,Node
import json


# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123"
# )

# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="m4eeee")

#整理原数据,整理为固定字段,并去重
with open('飞华疾病.json','r',encoding='utf-8') as file_name:
    # file_names = list(file_name.read())
    file_data = file_name.read()
    json_data = json.loads(file_data)  #dict
    json_list = json_data['RECORDS']   #[{},{}]

ready_dict = []
for dict in json_list:
    dict_data = {}
    dict_data['名称'] = dict.get('title','空')
    dict_data['部位'] = dict.get('pathogenic_site','暂无数据').split('、')
    dict_data['科室'] = dict.get('Clinical_Cente','暂无数据').split('、')   #list
    dict_data['症状'] = dict.get('classical_symptom','暂无数据').split('、')  #list
    crx = dict.get('infectious')
    if crx =='该病具有传染性':
        dict_data['传染性'] = True
    if crx == '该病不具有传染性':
        dict_data['传染性'] = False
    dict_data['多发人群'] = dict.get('High-risk_groups','暂无数据')
    dict_data['检查项目'] = dict.get('inspection_item','暂无数据').split('、')
    dict_data['定义'] = ''.join(dict.get('summarize','暂无数据').replace('"',"'").split())
    dict_data['病因'] = ''.join(dict.get('pathogenesis','暂无数据').replace('"',"'").split())
    dict_data['治疗方法详述'] = ''.join(dict.get('cure','暂无数据').replace('"',"'").split())
    dict_data['检查内容详述'] = ''.join(dict.get('examine','暂无数据').replace('"',"'").split())
    dict_data['预防详述'] = ''.join(dict.get('prevent','暂无数据').replace('"',"'").split())
    dict_data['饮食保健'] = ''.join(dict.get('diet','暂无数据').replace('"',"'").split())

    if dict_data not in ready_dict:
        ready_dict.append(dict_data)

json_dict = json.dumps(ready_dict, ensure_ascii=False)
with open('feihuadisease.json','wb') as ff:
    ff.write(json_dict.encode('utf-8'))

with open('feihuadisease.json','r',encoding='utf-8') as f:
    content = f.read()
    content = json.loads(content)   #[{},{},{}]
    print(len(content))
    # print(content[0])


# # 将原数据去重
json_names = []
for dict in content:
    json_names.append(dict['名称'])
print(len(json_names))
# print(len(json_dicts))
#
# # 查询数据库中疾病，找出库中没有的疾病
# #
cql = "match (n:疾病) return n.名称"
neo_name = graph.run(cql).data()  #list
neo_names = []
for dict in neo_name:
    neo_names.append(dict['n.名称'])
print(len(neo_names))
print(len(set(neo_names)))
#
#
# # 分析原数据，准备入库
# #TODO 现在库中不包含的疾病不入库
# # 先准备库中已有疾病数据：
todo_data = set(json_names) - set(neo_names)
print(len(todo_data))
ready_data = list(set(json_names) - todo_data)   #名字列表
print(len(ready_data))
print(ready_data)
#

# 对要处理的数据进行处理：包括已有和没有的：
jbn = 0
zzn = 0
bwn = 0
ksn = 0
jcn = 0
for name in ready_data:
    for dict in content:
        if dict['名称'] != name:
            continue
        else:
            tmp_dict = dict

    # cql = """match (n:疾病{名称:'%s'}) return n.名称 """%name
    # neo_node = graph.run(cql).data()
        neo_node = graph.find_one(label="疾病", property_key="名称", property_value=name)
        if neo_node: #如果有此疾病节点
            #更新标签和属性
            sql = """match (n:疾病{名称:'%s'}) set n:飞华"""%name
            graph.run(sql)
            if neo_node.get('传染性','暂无数据') == '暂无数据':
                sql = """match (n:疾病) where n.名称='%s' set n.传染性="%s" """%(name,tmp_dict['传染性'])
                print(sql)
                graph.run(sql)
            if neo_node.get('多发人群','暂无数据') == '暂无数据':
                # sql = """match (n:疾病{名称:'%s'}) set n.多发人群='%s'"""%(name,tmp_dict['多发人群'])
                sql = """match (n:疾病) where n.名称='%s' set n.多发人群="%s" """%(name,tmp_dict['多发人群'])

                print(sql)
                graph.run(sql)
            if neo_node.get('定义','暂无数据') == '暂无数据':
                # sql = """match (n:疾病{名称:'%s'}) set n.定义='%s'"""%(name,tmp_dict['定义'])
                sql = """match (n:疾病) where n.名称='%s' set n.定义="%s" """%(name,tmp_dict['定义'])

                print(sql)
                graph.run(sql)
            if neo_node.get('治疗方法详述','暂无数据') == '暂无数据':
                # sql = """match (n:疾病{名称:'%s'}) set n.治疗方法详述="%s" """%(name,tmp_dict['治疗方法详述'])
                sql = """match (n:疾病) where n.名称='%s' set n.治疗方法详述="%s" """%(name,tmp_dict['治疗方法详述'])

                print(sql)
                graph.run(sql)
            if neo_node.get('检查内容详述','暂无数据') == '暂无数据':
                # sql = """match (n:疾病{名称:'%s'}) set n.检查内容详述="%s" """%(name,tmp_dict['检查内容详述'])
                sql = """match (n:疾病) where n.名称='%s' set n.检查内容详述="%s" """%(name,tmp_dict['检查内容详述'])

                print(sql)
                graph.run(sql)
        else:  # 如果不存在该疾病节点，则新建节点
               # 创建疾病节点
            node_jb = Node('疾病', '飞华', 传染性=tmp_dict['传染性'], 多发人群=tmp_dict['多发人群'], 名称=tmp_dict['名称'], 定义=tmp_dict['定义'],治疗方法详述=tmp_dict['治疗方法详述'],检查内容详述=tmp_dict['检查内容详述'])
            graph.merge(node_jb)
            jbn += 1
            print('jb%s'%jbn)

        #更新科室
        if tmp_dict['科室'] != '暂无数据':
            for ks in tmp_dict['科室']:
                cql = """match (n:科室{名称:'%s'}) return n.名称"""%(ks)
                res_ks = graph.run(cql).data()
                if res_ks:
                    sql = "MATCH (n:`科室`{名称:'%s'}) set n:飞华" % (ks)
                    graph.run(sql)
                else:
                    node_ks = Node('科室', '飞华', 名称=ks)
                    graph.merge(node_ks)
                    ksn += 1
                    print('科室%s,%s'%(ksn,ks))

                # 并在疾病和科室之间创建关系
                # query = """match(p:%s{名称:"%s"}),(q:%s{名称:"%s"}) merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                #     '疾病', tmp_dict['名称'],'科室', ks, '科室', '科室')
                query = """match(p:%s),(q:%s) where p.名称="%s" and q.名称="%s" merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                    '疾病', '科室', tmp_dict['名称'], ks, '科室', '科室')
                graph.run(query)

#
        # 更新部位
        if tmp_dict['部位'] != '暂无数据':
            for bw in tmp_dict['部位']:
                if bw == '头部':
                    bw = '头'
                if bw == '手部':
                    bw = '手'
                if bw == '面部':
                    bw = '面'
                if bw == '鼻部':
                    bw = '鼻'
                if bw == '耳部':
                    bw = '耳'
                if bw ==  '足部':
                    bw = '足'
                cql = """match (n:部位{名称:'%s'}) return n.名称"""%(bw)
                res_bw = graph.run(cql).data()
                if res_bw:
                    sql = "MATCH (n:`部位`{名称:'%s'}) set n:飞华" % (bw)
                    graph.run(sql)
                else:
                    node_bw = Node('部位', '飞华', 名称=bw)
                    graph.merge(node_bw)
                    bwn += 1
                    print('部位%s,%s'%(bwn,bw))
                # 并在疾病和部位之间创建关系
                # query = """match(p:%s{名称:"%s"}),(q:%s{名称:"%s"}) merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                #     '疾病', tmp_dict['名称'], '部位', bw, '部位', '部位')
                query = """match(p:%s),(q:%s) where p.名称="%s" and q.名称="%s" merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                    '疾病', '部位', tmp_dict['名称'], bw, '部位', '部位')
                graph.run(query)

        #更新症状
        if tmp_dict['症状'] != '暂无数据':
            for zz in tmp_dict['症状']:
                cql = """match (n:症状{名称:'%s'}) return n.名称"""%(zz.strip())
                res_zz = graph.run(cql).data()
                print(cql)
                if res_zz:
                    sql = "MATCH (n:症状{名称:'%s'}) set n:飞华" % (zz.strip())
                    graph.run(sql)
                else:
                    node_zz = Node('症状', '飞华', 名称=zz.strip())
                    graph.merge(node_zz)
                    zzn += 1
                    print('症状%s,%s'%(zzn,zz))
                # 并在疾病和症状之间创建关系
                # query = """match(p:%s{名称:"%s"}),(q:%s{名称:"%s"}) merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                #     '疾病', tmp_dict['名称'], '症状',  zz, '症状', '症状')
                query = """match(p:%s),(q:%s) where p.名称="%s" and q.名称="%s" merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                    '疾病', '症状', tmp_dict['名称'], zz, '检查项目', '检查项目')
                graph.run(query)

        #更新检查项目
        if tmp_dict['检查项目'] != '暂无数据':
            for jc in tmp_dict['检查项目']:
                cql = """match (n:检查项目{名称:'%s'}) return n.名称"""%(jc)
                res_jc = graph.run(cql).data()
                if res_jc:
                    sql = "MATCH (n:`检查项目`{名称:'%s'}) set n:飞华" % (jc)
                    graph.run(sql)
                else:
                    node_jc = Node('检查项目', '飞华', 名称=jc)
                    graph.merge(node_jc)
                    jcn += 1
                    print('检查%s,%s'%(jc,jcn))
                # 并在疾病和症状之间创建关系
                # query = """match(p:%s{名称:"%s"}),(q:%s{名称:"%s"}) merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                #     '疾病',  tmp_dict['名称'], '检查项目', jc, '检查项目', '检查项目')
                query = """match(p:%s),(q:%s) where p.名称="%s" and q.名称="%s" merge (p)-[rel:%s{名称:"%s"}]->(q)""" % (
                        '疾病', '检查项目',tmp_dict['名称'], jc, '检查项目', '检查项目')
                graph.run(query)
                print(query)


