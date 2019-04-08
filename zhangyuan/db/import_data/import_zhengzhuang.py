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

def import_zhengzhuang(file,laiyuan):
    with open(file,'r',encoding='utf-8') as ff1:
        content = ff1.read()
        json_data = json.loads(content)  #[]
        n=0
        for dict in json_data:
            n+=1
            print(dict['名称'])
            print(n)
            print(dict.get('别名'))
            a = graph.find_one(label="症状",property_key = "名称", property_value = dict['名称'])
            if a:
                cql = """match (n:症状) where n.名称 = "%s" set n:%s"""%(dict.get('名称','').replace('"',"'").replace('\\','\\\\'),laiyuan)
                graph.run(cql)
                if a.get('图片', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`症状`) where n.名称="%s" set n.图片="%s" """ % (dict['名称'].replace('"',"'").replace('\\','\\\\'), dict.get('英文名称','暂无数据').replace('"',"'"))
                    graph.run(sql)
                if a.get('别名', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`症状`) where n.名称="%s" set n.别名=%s """ % (dict['名称'].replace('"',"'").replace('\\','\\\\'), dict.get('别名','暂无数据'))
                    graph.run(sql)
                if a.get('定义', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`症状`) where n.名称="%s" set n.定义="%s" """ % (dict['名称'].replace('"',"'").replace('\\','\\\\'), dict.get('定义','暂无数据').replace('"',"'").replace('\\','\\\\'))
                    graph.run(sql)
                if a.get('url', '暂无数据') == '暂无数据':
                    sql = """MATCH (n:`症状`) where n.名称="%s" set n.url="%s" """ % (dict['名称'].replace('"',"'").replace('\\','\\\\'), dict.get('url','暂无数据').replace('"',"'").replace('\\','\\\\'))
                    graph.run(sql)


            else:
                node_dict = Node('症状', laiyuan, 名称=dict['名称'].replace('\\','\\\\'),图片=dict['图片'],别名=dict['别名'],定义=dict['定义'],url=dict['url'])
                graph.merge(node_dict)

            #更新关系-部位
            for bw in dict.get('部位','暂无数据'):
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


                    cql = """match (n:部位) where n.名称="%s" return n.名称 """%bw
                    m = graph.run(cql)
                    if m:
                        query = """match (n:症状),(m:部位) where n.名称="%s" and m.名称="%s" merge (n)-[r:部位{名称:"部位"}]->(m) """%(dict.get('名称','').replace('\\','\\\\'),bw)
                        graph.run(query)
                    else:
                        node_d = Node('部位',名称=bw)
                        graph.merge(node_d)

            #更新关系-科室
            for ks in dict.get('科室','暂无数据'):
                if ks != '暂无数据':
                    cql = """match (n:科室) where n.名称="%s" return n.名称 """%ks
                    m = graph.run(cql)
                    if m:
                        query = """match (n:症状),(m:科室) where n.名称="%s" and m.名称="%s" merge (n)-[r:科室{名称:"科室"}]->(m) """%(dict.get('名称','').replace('\\','\\\\'),ks)
                        graph.run(query)
                    else:
                        node_d = Node('科室', 名称=ks)
                        graph.merge(node_d)

            #更新关系-症状
            for zz in dict.get('相似症状','暂无数据'):
                if zz != '暂无数据':
                    cql = """match (n:症状) where n.名称="%s" return n.名称 """%zz
                    m = graph.run(cql)
                    if m:
                        query = """match (n:症状),(m:症状) where n.名称="%s" and m.名称="%s" merge (n)-[r:相似症状{名称:"相似症状"}]->(m) """%(dict.get('名称','').replace('\\','\\\\'),zz)
                        graph.run(query)

            #更新关系-疾病
            for jb in dict.get('疾病','暂无数据'):
                if jb != '暂无数据':
                    cql = """match (n:疾病) where n.名称="%s" return n.名称 """%jb
                    m = graph.run(cql)
                    if m:
                        query = """match (n:症状),(m:疾病) where n.名称="%s" and m.名称="%s" merge (n)<-[r:症状{名称:"症状"}]-(m) """%(dict.get('名称','').replace('\\','\\\\'),jb)
                        graph.run(query)

            #更新关系-检查项目
            for jc in dict.get('检查项目','暂无数据'):
                if jc != '暂无数据':
                    cql = """match (n:检查项目) where n.名称="%s" return n.名称 """%jc
                    m = graph.run(cql)
                    if m:
                        query = """match (n:症状),(m:检查项目) where n.名称="%s" and m.名称="%s" merge (n)-[r:检查项目{名称:"检查项目"}]->(m) """%(dict.get('名称','').replace('\\','\\\\'),jc)
                        graph.run(query)


            #更新关系-通用药品
            tyyp = dict.get('通用药品','暂无数据')
            if tyyp != '暂无数据':
                cql = """match (n:药品通用名称) where n.名称="%s" return n.名称 """%tyyp
                m = graph.run(cql)
                if m:
                    query = """match (n:症状),(m:药品通用名称) where n.名称="%s" and m.名称="%s" merge (n)-[r:药品通用名称{名称:"药品通用名称"}]->(m) """%(dict.get('名称','').replace('\\','\\\\'),tyyp)
                    graph.run(query)


            #更新关系-药品
            for yp in dict.get('药品','暂无数据'):
                if yp != '暂无数据':
                    cql = """match (n:药品) where n.名称="%s" return n.名称 """%yp
                    m = graph.run(cql)
                    if m:
                        query = """match (n:症状),(m:药品) where n.名称="%s" and m.名称="%s" merge (n)-[r:药品{名称:"药品"}]->(m) """%(dict.get('名称','').replace('\\','\\\\'),yp)
                        graph.run(query)

if __name__ == '__main__':
    # import_zhengzhuang('/Users/zhangyuan/work/爬虫数据/9939/9939_zhengzhuang_ready.json','九九三九')
    # import_zhengzhuang('/Users/zhangyuan/work/爬虫数据/全球医院/qqyy_zhengzhuang_ready.json','全球医院')
    # import_zhengzhuang('/Users/zhangyuan/work/爬虫数据/健康一线/jkyx_zhengzhuang_ready.json','健康一线')  #7175
    import_zhengzhuang('/Users/zhangyuan/work/爬虫数据/名医在线/myzx_zhengzhuang_ready.json','名医在线')  #2828条数据
