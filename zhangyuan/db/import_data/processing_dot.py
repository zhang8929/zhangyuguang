import json
from py2neo import Graph

# 本地测试库
# graph = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123",
#             secure=False,
#             bolt=False,
# )
# graph = Graph(
#             host="154.8.214.203",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="m4eeee",
#             secure=False,
#             bolt=False,)

def feihuadot_zz():

    list1=[]
    with open ('../prepare_data/feihuadot_zz.txt','r',encoding='utf-8') as file:
        contents = file.readlines()
        # print(contents)
        zz_list = []
        for content in contents:
            zz_list.append(content[:-1])
        # print(type(contents))

        with open (r'D:\nlp\医疗\爬虫数据\飞华\feihuadot_zz.json','r',encoding='utf-8') as file:
            str_data = file.read()
            json_data = json.loads(str_data)
            print(type(json_data['RECORDS']))  #【{}，{}】
            json_list = []
            for dict in json_data['RECORDS']:
                json_list.append(dict['title'])


            for dotzz in zz_list:
                for jsons in json_data['RECORDS']:
                    if dotzz == jsons['title']:
                        print(dotzz)
                        cql = """match (n:症状) where n.名称='%s' set n.定义="%s" """ % (dotzz,jsons['intro'].strip().replace('"',"'"))
                        graph.run(cql)

# feihuadot_zz()
def jb_dot():
    list1 = []
    with open('../prepare_data/jbdot.txt', 'r', encoding='utf-8') as file:
        contents = file.readlines()
        # print(contents)
        jb_list = []
        for content in contents:
            jb_list.append(content[:-1])
        # print(type(contents))

        with open(r'D:\nlp\医疗\爬虫数据\寻医问药\xunyiwenyao_1.json', 'r', encoding='utf-8') as file:
            str_data = file.read()
            json_data = json.loads(str_data)
            print(type(json_data['RECORDS']))  # 【{}，{}】
            json_list = []
            for dict in json_data['RECORDS']:
                json_list.append(dict['title'])



            for jbdot in jb_list:
                for jsons in json_data['RECORDS']:
                    if jbdot == jsons['title']:
                        list1.append(jbdot)
                        print(jbdot)
                        cql = """match (n:疾病) where n.名称='%s' set n.病症详述="%s" """ % (jbdot, jsons['symptom'].replace('"', "'"))
                        graph.run(cql)


            print(len(list1))


def dotzz():

    list1 = []
    dict = {}
    with open('../tmp.txt', 'r', encoding='utf-8') as file:
        zzs = file.readlines()

        with open(r'D:\nlp\医疗\爬虫数据\寻医问药\xywy_zz.json', 'r', encoding='utf-8') as f:
            content = f.read()
            json_data = json.loads(content)

            for dotzz in zzs:
                for jsons in json_data:
                    # if dotzz == '脓液为巧克力色':
                    # print(dotzz)
                    # print(json['名称'])
                    if dotzz[:-1] in jsons['名称']:
                        # dict['key'] = dotzz[:-1]
                        # dict['value'] = json['名称'][:-1]
                        # list1.append(dict)
                        # print(json['名称']+'---'+dotzz[:-1])
                        dict[dotzz[:-1]] = jsons['名称']
                        list1.append(dict)

    print(len(list1))
    print(len(list1[0]))
    # print([list1[0]])
    for name in list1[0].keys():
        value = list1[0][name]
        name = name + '...'

        cql = """match (n:症状) where n.名称 = "%s" set n.名称="%s" """ % (name, value)
        graph.run(cql)
        print(cql)

def renqun_dot():
    list1 = []
    dict = {}
    with open('./dot_renqun.txt', 'r', encoding='utf-8') as file:
        jbs = file.readlines()

        with open(r'D:\nlp\医疗\爬虫数据\寻医问药\xywy_jb_renqun.json', 'r', encoding='utf-8') as f:
            content = f.read()
            json_data = json.loads(content)

            for jb in jbs:
                for jsons in json_data:

                    if jb[:-1] == jsons['名称']:
                        dict[jb[:-1]] = jsons['多发人群']
                        # print(dict)
                        # print(jb[:-1]+'------'+json['名称'])
                        list1.append(dict)

    print(len(list1))
    print(len(list1[0]))
    # print([list1[0]])
    for name in list1[0].keys():
        value = list1[0][name]

        cql = """match (n:疾病) where n.名称 = "%s" set n.多发人群="%s" """ % (name, value)
        graph.run(cql)
        print(cql)

def baike_renqun():
    with open(r'D:\nlp\医疗\爬虫数据\baike_renqun.json', 'r', encoding='utf-8') as f:
        content = f.read()
        # print(type(content))
        json_data = json.loads(content,encoding='utf-8')
        for dict in json_data:
            name = dict['名称']
            renqun = dict.get('多发群体','暂无数据')
            cql = """match (n:疾病) where n.名称="%s" set n.多发人群="%s" """%(name, renqun)
            graph.run(cql)
            print(cql)

if __name__ == '__main__':
    # jb_dot()
    # feihuadot_zz()
    # dotzz()
    # renqun_dot()
    baike_renqun()