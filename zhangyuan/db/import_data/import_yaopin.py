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
graph = Graph(
            host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="m4eeee",
            secure=False,
            bolt=False,)


def import_yaopin(file,laiyuan,):
    with open(file,'r',encoding='utf-8') as file:
        content = file.read()
        json_data = json.loads(content)
        n = 0
        for dict in json_data:
            print(dict['名称'])
            n+=1
            print(n)
            a = graph.find_one(label="药品", property_key="名称", property_value=dict['名称'])
            if a: #库中有，去拿属性
                sql = "MATCH (n:`药品`{名称:'%s'}) set n:%s" % (dict['名称'],laiyuan)
                graph.run(sql)
                if a.get('英文名称', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.英文名称="%s" """ % (dict['名称'], dict.get('英文名称','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('制药公司', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.制药公司="%s" """ % (dict['名称'], dict.get('制药公司','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('处方药', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.处方药="%s" """ % (dict['名称'], dict.get('处方药','是').replace('"',"'"))
                    graph.run(sql)
                if a.get('药品类别', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.药品类别="%s" """ % (dict['名称'], dict.get('药品类别','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('用法用量', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.用法用量="%s" """ % (dict['名称'], dict.get('用法用量','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('适用症描述', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.适用症描述="%s" """ % (dict['名称'], dict.get('适用症描述','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('特殊人群用药', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.特殊人群用药="%s" """ % (dict['名称'], dict.get('特殊人群用药','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('禁忌', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.禁忌="%s" """ % (dict['名称'], dict.get('禁忌','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.成分="%s" """ % (dict['名称'], dict.get('成分','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('注意事项', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.注意事项="%s" """ % (dict['名称'], dict.get('注意事项','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('不良反应', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.不良反应="%s" """ % (dict['名称'], dict.get('不良反应','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('有效期', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.有效期="%s" """ % (dict['名称'], dict.get('有效期','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('药物相互作用', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.药物相互作用="%s" """ % (dict['名称'], dict.get('药物相互作用','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('图片', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.图片="%s" """ % (dict['名称'], dict.get('图片','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('医保', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.医保="%s" """ % (dict['名称'], dict.get('医保','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)
                if a.get('url', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`药品`) where n.名称='%s' set n.url="%s" """ % (dict['名称'], dict.get('url','暂无数据').replace('"',"'"))
                    # print(sql)
                    graph.run(sql)


            else: #说明没有这个点，新增节点
                node_dict = Node('药品', laiyuan, 名称=dict['名称'], 英文名称=dict.get('英文名称','暂无数据'), 批准文号=dict.get('批准文号','暂无数据'),
                                  制药公司=dict.get('制药公司','暂无数据'), 处方药=dict.get('处方药','是'), 药品类别=dict.get('药品类别','暂无数据'),
                                  用法用量=dict.get('用法用量','暂无数据'), 适用症描述=dict.get('适用症描述','暂无数据'), 特殊人群用药=dict.get('特殊人群用药','暂无数据'),
                                  成分=dict.get('成分','暂无数据'),禁忌=dict.get('禁忌','暂无数据'),注意事项=dict.get('注意事项','暂无数据'),不良反应=dict.get('不良反应','暂无数据'),
                                  有效期=dict.get('有效期','暂无数据'),药物相互作用=dict.get('药物相互作用','暂无数据'),图片=dict.get('图片','暂无数据'),
                                 医保=dict.get('医保','暂无数据'),url=dict.get('url'))
                graph.merge(node_dict)



            #创建药品通用名称节点：
            ty_mc = dict['药品通用名称']
            cql = """match (n:药品通用名称) where n.名称="%s" return n.名称"""%ty_mc
            res = graph.run(cql).data()
            if res:#如果找到这个通用药品名称：
                cql = """match (n:药品通用名称) where n.名称="%s" set n:%s"""%(ty_mc,laiyuan)
                graph.run(cql)
                query = """match (n:药品),(m:药品通用名称) where n.名称="%s" and m.名称="%s" merge (n)<-[r:药品产品{名称:'药品产品'}]-(m)"""%(dict['名称'],ty_mc)
                graph.run(query)
            else:#如果没找到通用名称
                tymc_node = Node(laiyuan,'药品通用名称',名称=ty_mc)
                graph.merge(tymc_node)
                query = """match (n:药品),(m:药品通用名称) where n.名称="%s" and m.名称="%s" merge (n)<-[r:药品产品{名称:'药品产品'}]-(m)"""%(dict['名称'],ty_mc)
                graph.run(query)

            # 开始更新关系--药品通用名称，疾病，症状
            for jb in dict['适用疾病']:
                if jb != '暂无数据':
                    sql = "MATCH (n:`疾病`{名称:'%s'}) RETURN n.名称" % (jb)
                    m = graph.run(sql).data()
                    if m:  # 如果匹配到了疾病节点
                        # sql = "MATCH (n:`疾病`{名称:'%s'}) set n:宝芝林" % (jb)
                        # graph.run(sql)
                        query1 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                            '疾病', '药品', jb, dict['名称'], '药品', '药品')
                        # print(query1)
                        graph.run(query1)
                        query2 = """match (n:疾病),(m:药品通用名称) where n.名称="%s" and m.名称="%s" merge (n)-[r:通用药品{名称:"通用药品"}]->(m)"""%(jb,ty_mc)
                        graph.run(query2)
                        # print(query2)

            #  更新症状关系
            for zz in dict.get('适用症状','暂无数据'):
                if zz != '暂无数据':
                    sql = "MATCH (n:`症状`{名称:'%s'}) RETURN n.名称" % (zz)
                    m = graph.run(sql).data()
                    if m:  # 如果匹配到了症状节点
                        # sql = "MATCH (n:`症状`{名称:'%s'}) set n:宝芝林" % (zz)
                        # graph.run(sql)=-0000-
                        query1 = "match(p:%s),(q:%s) where p.名称='%s'and q.名称='%s' merge (p)-[rel:%s{名称:'%s'}]->(q)" % (
                            '症状', '药品', zz, dict['名称'], '药品', '药品')
                        graph.run(query1)
                        query2 = """match (n:症状),(m:药品通用名称) where n.名称="%s" and m.名称="%s" merge (n)-[r:通用药品{名称:"通用药品"}]->(m)""" % (zz, ty_mc)
                        graph.run(query2)


if __name__ == '__main__':
    # import_yaopin('../prepare_data/宝芝林_药品_ready.json')
    # import_yaopin('../prepare_data/kswys_yp_ready.json')
    # import_yaopin('../prepare_data/new6_ready.json')
    # import_yaopin('../prepare_data/minfu_ready.json','民福康')  #663条数据
    import_yaopin('/Users/zhangyuan/work/爬虫数据/家庭医生/jtys_ready_5.json','家庭医生')  #47509条数据




