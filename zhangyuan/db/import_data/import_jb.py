from py2neo import Graph,Node
import json

# 本地测试库
# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123",
#             secure=False,
#             bolt=False,
# )
#
# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="m4eeee",
#             secure=False,
#             bolt=False,)


def import_jibing(file,laiyuan):
    with open(file,'r',encoding='utf-8') as file:
        content = file.read()
        json_data = json.loads(content)
        n = 0
        for dict in json_data:
            print(dict['名称'])
            n+=1
            print(n)
            a = graph.find_one(label="疾病", property_key="名称", property_value=dict['名称'])
            if a:
                sql = """match (n:疾病) where n.名称="%s" set n:%s"""%(dict.get('名称','').replace('"',"'"),laiyuan)
                graph.run(sql)


                property_key = ['英文名','定义','病因','多发人群','治疗方法详述','治疗费用','医保','传染性','传染方式','患病比例',
                                '患病比例值','治愈率','治愈率值','治疗周期','温馨提示','鉴别详述','预防详述','饮食保健','检查内容详述',
                                '病症详述','护理详述','url']
                key_list = []
                for pro_key in property_key:
                    value = a.get(pro_key,'暂无数据')
                    if value == '暂无数据':
                        key_list.append(pro_key)

                print(key_list)

                if len(key_list) != 0:
                    sql = """match (n:疾病) where n.名称="%s" set """%(dict['名称'].replace('"', "'"))
                    for key in key_list:
                        sql += """n.%s = "%s", """%(key,dict.get(key,'暂无数据').replace('"',"'").strip().replace('\\','\\\\'))
                    sql = sql[:-2]
                print(sql)
                graph.run(sql)

                if a.get('别称','暂无数据') == '暂无数据':
                    sql = """MATCH (n:`疾病`) where n.名称="%s" set n.别称=%s """ % (dict['名称'].replace('"', "'"), dict.get('别称', ['暂无数据']))
                    graph.run(sql)
                    print(sql)
                # list1 = a.get('别称','暂无数据')
                # print(type(list1))
                # alias_list = json.loads(list1)
                # print((dict.get('别称', ['暂无数据'])))
                # for i in dict.get('别称',['暂无数据']):
                #
                #     if i.strip() not in alias_list:
                #         alias_list.append(i.strip())
                # print('1')
                # cql = """match (n:疾病) where n.名称 = "%s" set n.别称="%s" """%(dict['名称'].replace('"',"'"),alias_list)
                # print(cql)
                # graph.run(cql)

                #
                # if a.get('英文名','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.英文名称="%s" """ % (dict['名称'].replace('"', "'"), dict.get('英文名称', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('病因','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.病因="%s" set n.病因="%s" """ % (dict['名称'].replace('"', "'"), dict.get('病因', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('多发人群','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.多发人群="%s" """ % (dict['名称'].replace('"', "'"), dict.get('多发人群', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('治疗方法详述', '暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.治疗方法详述="%s" """ % (dict['名称'].replace('"', "'"), dict.get('治疗方法详述', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('治疗费用', '暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.治疗费用="%s" """ % (dict['名称'].replace('"', "'"), dict.get('治疗费用', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('医保','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.医保="%s" """ % (dict['名称'].replace('"', "'"), dict.get('医保', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('传染性','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.传染性="%s" """ % (dict['名称'].replace('"', "'"), dict.get('传染性', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('传染方式','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.传染方式="%s" """ % (dict['名称'].replace('"', "'"), dict.get('传染方式', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('患病比例','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.患病比例="%s" """ % (dict['名称'].replace('"', "'"), dict.get('患病比例', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('患病比例值','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.患病比例值="%s" """ % (dict['名称'].replace('"', "'"), dict.get('患病比例值', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('治愈率','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.治愈率="%s" """ % (dict['名称'].replace('"', "'"), dict.get('治愈率', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('治愈率值','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.治愈率值="%s" """ % (dict['名称'].replace('"', "'"), dict.get('治愈率值', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('治疗周期','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.治疗周期="%s" """ % (dict['名称'].replace('"', "'"), dict.get('治疗周期', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('温馨提示','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.温馨提示="%s" """ % (dict['名称'].replace('"', "'"), dict.get('温馨提示', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('鉴别详述','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.鉴别详述="%s" """ % (dict['名称'].replace('"', "'"), dict.get('鉴别详述', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('预防详述','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.预防详述="%s" """ % (dict['名称'].replace('"', "'"), dict.get('预防详述', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('饮食保健','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.饮食保健="%s" """ % (dict['名称'].replace('"', "'"), dict.get('饮食保健', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('检查内容详述','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.检查内容详述="%s" """ % (dict['名称'].replace('"', "'"), dict.get('检查内容详述', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('病症详述','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.病症详述="%s" """ % (dict['名称'].replace('"', "'"), dict.get('病症详述', '暂无数据').replace('"', "'"))
                #     graph.run(sql)
                # if a.get('护理详述','暂无数据') == '暂无数据':
                #     sql = """MATCH (n:`疾病`) where n.名称="%s" set n.护理详述="%s" """ % (dict['名称'].replace('"', "'"), dict.get('护理详述', '暂无数据').replace('"', "'"))
                #     graph.run(sql)





            else:
                print(dict['名称'])
                print('新增节点')
                node_dict = Node('疾病',laiyuan,名称=dict.get('名称',''),别称=dict.get('别称','暂无数据'),英文名=dict.get('英文名','暂无数据'),
                                 定义=dict.get('定义', '暂无数据'),病因=dict.get('病因','暂无数据'),多发人群=dict.get('多发人群','暂无数据'),
                                 治疗方法详述=dict.get('治疗方法详述', '暂无数据'),治疗费用=dict.get('治疗费用','暂无数据'),医保=dict.get('医保','暂无数据'),
                                 传染性=dict.get('传染性','暂无数据'),患病比例=dict.get('患病比例','暂无数据'),患病比例值=dict.get('患病比例值','暂无数据'),
                                 治愈率=dict.get('治愈率', '暂无数据'),治愈率值=dict.get('治愈率值','暂无数据'),治疗周期=dict.get('治疗周期','暂无数据'),
                                 温馨提示=dict.get('温馨提示', '暂无数据'),鉴别详述=dict.get('鉴别详述','暂无数据'),预防详述=dict.get('预防详述','暂无数据'),
                                 饮食保健=dict.get('饮食保健', '暂无数据'),检查内容详述=dict.get('检查内容详述','暂无数据'),病症详述=dict.get('病症详述','暂无数据'),
                                 护理详述=dict.get('护理详述', '暂无数据'),流行度=dict.get('流行度','暂无数据'))
                graph.merge(node_dict)

            # 更新关系-科室

            for ks in dict.get('科室', '暂无数据'):
                if ks != '暂无数据':
                    cql = """match (n:科室) where n.名称="%s" return n.名称 """ % ks
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:科室) where n.名称="%s" and m.名称="%s" merge (n)-[r:科室{名称:"科室"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), ks)
                        graph.run(query)
                    else:
                        node_d = Node('科室',laiyuan,名称=ks)
                        graph.merge((node_d))
            # 更新关系-部位
            for bw in dict.get('部位', '暂无数据'):
                if bw != '暂无数据':
                    if bw == '头部':
                        bw = '头'
                    if bw == '鼻部':
                        bw = '鼻'
                    if bw == '手部':
                        bw = '手'
                    if bw == '足部':
                        bw = '足'
                    if bw == '面部':
                        bw = '面'
                    if bw == '眼部':
                        bw = '眼'
                    cql = """match (n:部位) where n.名称="%s" return n.名称 """ % bw
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:部位) where n.名称="%s" and m.名称="%s" merge (n)-[r:部位{名称:"部位"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), bw)
                        graph.run(query)

            # 更新关系-zz
            for zz in dict.get('症状', '暂无数据'):
                if zz != '暂无数据':
                    cql = """match (n:症状) where n.名称="%s" return n.名称 """ % zz
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:症状) where n.名称="%s" and m.名称="%s" merge (n)-[r:症状{名称:"症状"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), zz)
                        graph.run(query)

            # 更新关系-jc
            for jc in dict.get('检查项目', '暂无数据'):
                if jc != '暂无数据':
                    cql = """match (n:检查项目) where n.名称="%s" return n.名称 """ % jc
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:检查项目) where n.名称="%s" and m.名称="%s" merge (n)-[r:检查项目{名称:"检查项目"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), jc)
                        graph.run(query)

            # 更新关系-jb
            for jb in dict.get('并发疾病', '暂无数据'):
                if jb != '暂无数据':
                    cql = """match (n:疾病) where n.名称="%s" return n.名称 """ % jb
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:疾病) where n.名称="%s" and m.名称="%s" merge (n)-[r:并发疾病{名称:"并发疾病"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), jb)
                        graph.run(query)

            # 更新关系-zl
            for zl in dict.get('治疗方法', '暂无数据'):
                if zl != '暂无数据':
                    cql = """match (n:治疗方法) where n.名称="%s" return n.名称 """ % zl
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:治疗方法) where n.名称="%s" and m.名称="%s" merge (n)-[r:治疗方法{名称:"治疗方法"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), zl)
                        graph.run(query)

            # 更新关系-yp
            for yp in dict.get('药品', '暂无数据'):
                if yp != '暂无数据':
                    cql = """match (n:药品) where n.名称="%s" return n.名称 """ % yp
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:药品) where n.名称="%s" and m.名称="%s" merge (n)-[r:药品{名称:"药品"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), yp)
                        graph.run(query)

            # 更新关系-zz
            for tyyp in dict.get('通用药品', '暂无数据'):
                if tyyp != '暂无数据':
                    cql = """match (n:药品通用名称) where n.名称="%s" return n.名称 """ % tyyp
                    m = graph.run(cql)
                    if m:
                        query = """match (n:疾病),(m:药品通用名称) where n.名称="%s" and m.名称="%s" merge (n)-[r:药品通用名称{名称:"药品通用名称"}]->(m) """ % (dict.get('名称', '').replace('"',"'"), tyyp)
                        graph.run(query)

if __name__ == '__main__':
    # import_jibing('/Users/zhangyuan/work/爬虫数据/9939/rest_ready.json','九九三九')
    # import_jibing('/Users/zhangyuan/work/爬虫数据/全球医院/qqyy_jibing_ready.json','全球医院')
    # import_jibing('/Users/zhangyuan/work/爬虫数据/健康度和微医/weiyi_ready.json','微医') #267
    # import_jibing('/Users/zhangyuan/work/爬虫数据/健康度和微医/jiankangdu_ready.json','健康度')  #10845 条数据
    # import_jibing('/Users/zhangyuan/work/爬虫数据/健康一线/jkyx_jibing_ready.json','健康一线') #6838条
    import_jibing('/Users/zhangyuan/work/爬虫数据/名医在线/myzx_jb_ready.json','名医在线')  #5337条

