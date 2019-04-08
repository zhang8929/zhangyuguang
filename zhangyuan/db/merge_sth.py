"""
为线上图库中的部位做整合处理
若A,B整合，则将A的所有节点查询出来，增加到B节点，并将A节点的所有东西删除--弃:要去重
将A,B两点都查出来，然后去重，增加到新节点
"""
from py2neo import Node, Relationship, Graph
from pandas import DataFrame
import json
# import codecs
import re

# 本地测试库
graph = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123",
            secure = False,
            bolt = False,
)

'''合并部位'''
def merge_location(node_1,node_2,new_node):
    #拿标签，创建新节点时候用

    # TODO 考虑应用事务保证操作一致性。


    cql = """match (n:部位) where n.名称='%s' or n.名称='%s' return labels(n)"""%(node_1,node_2)
    labels = graph.run(cql).data()
    print(labels)
    value = []
    for label in labels:
        value += label['labels(n)']

    label = list(set(value))
    # print(len(label))


    # 拿关系的起止点保存
    file_name = 'node_%s.json' % new_node
    cql = """MATCH (n:部位)<-[r]-(m) where n.名称='%s' or n.名称='%s' return r,m.名称,labels(m),id(m)"""%(node_1,node_2)
    nodes = graph.run(cql).data()
    print('-----%s'%(len(nodes)))

    js_nodes = json.dumps(nodes, ensure_ascii=False)

    with open(file_name, 'wb') as ff:
        ff.write(js_nodes.encode('utf-8'))

    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        nodes = json.loads(content)  #list
        print(len(nodes))
    ready_node = []
    for node in nodes:
        if node not in ready_node:
            ready_node.append(node)
    print(len(ready_node))
    # print(ready_node)

    # 删除原有节点，新建节点，并创建关系
    delete="""match (n:部位)<-[r]-(m) where n.名称='%s' or n.名称='%s' delete n,r"""%(node_1,node_2)   #TODO 若没有关系这条语句删除不了节点
    print(delete)
    graph.run(delete)
    node_add = """create (n:"""
    for lab in label:
        node_add += lab
        node_add += ':'
    node_add = node_add[:-1]+"{名称:'%s'})"%new_node
    graph.run(node_add)
    print(node_add)

    print(len(ready_node))
    n=0
    for node in ready_node:
        if '疾病' in node['labels(m)']:
            # labels = str(node['labels(m)'])[1:-1].replace("'","").replace(',',':')
            query1 = "match(p:部位{名称:'%s'}),(q:疾病{名称:'%s'}) where id(q) = %s merge (p)<-[rel:%s{名称:'%s'}]-(q)" % (
                new_node,node['m.名称'],node['id(m)'],'部位', '部位')
            print(query1)
            n += 1
            print(n)
            graph.run(query1)
        if '症状' in node['labels(m)']:
            # labels = str(node['labels(m)'])[1:-1].replace("'","").replace(',',':')
            query1 = "match(p:部位{名称:'%s'}),(q:症状{名称:'%s'}) where id(q) = %s merge (p)<-[rel:%s{名称:'%s'}]-(q)" % (
                new_node,node['m.名称'], node['id(m)'],'部位', '部位')
            print(query1)
            n+=1
            print(n)
            graph.run(query1)


'''合并症状'''
def merge_symptom():
    #拿标签，创建新节点时候用

    # TODO 考虑应用事务保证操作一致性。

    symptom_lists = [
        '肺部转移', '肚脐疼', '排便困难', '舌短声哑', '全身皮肤充血', '水冲脉', '情绪不宁', '颈部僵硬', '肝被膜血肿破裂', '黑痣', '氧分压低',
        '胃纳差', '脉率增快', '尿道瓣', '无力', '无脉症', '泌尿道破裂', '胀痛', '神经根激惹症状', '横结肠移位', '肝星状细胞增生', '肾络滞阻',
        '轻度痛', '温觉丧失', '弱视眼的拥挤现象', '大动脉错位', '过渡区R波递增不良', '腹部型肥胖', '搏动性肿块', '骨髓浆细胞增多',
        '溃疡外观呈菜花样', '呻吟', '冠状动脉供血不足', '心包压塞', '肝细胞内脂肪堆积过多', '压榨样绞痛', '行为无计划性', '弥漫性腹部骨化',
        '骨骼停止发育', '潮红潮热', '脊髓内空洞形成', '营养性皮肤改变', '胃食管反流症状', '血糖值升高', '血管神经性水肿',
        '皮疹呈瘀点', '耳鸣如潮', '先天性乳糖不耐受', '骨转移', '骨骼肿块', '腹肌紧张', '维生素K缺乏', '黏液尿', 'HIV感染', '肝细胞坏死',
        '淋巴液流出', '洪脉', '颈部粗', '气不摄血', '皮肤痛', '动静脉短路现象', '内分泌功能减退', '泛发性红色斑块', '肉芽肿', '皮肤硬化', '不排胎便',
        '黏膜损害', '炎性细胞浸润', '耳道流脓', '眼底出血和渗出', '憩室出血', '脘痞腹胀', '突发性疼痛', '黏液便', '奇脉', '夸大狂',
        '胃肠淋巴回流受阻', '手麻', '肾气虚', '钙离子内流', '颈部搏动', '血管杂音', '儿童联想和情感障碍', '突肤挺胸', '血管性头痛',
        '脊髓梗死', '胎样心音', '颈部肿块', '高渗尿', '吸气时有蝉鸣音', '代脉', '耐热力降低', '胀坠感', '皮肤有瘙痒抓痕',
        '皮肤龟裂', '心理伤害', '情绪性腹痛', '无症状型溃疡', '冠状动脉痉挛', '缺氧缺血性神经损伤', '骶尾部急性脓肿', '普秃',
        '恶病性痤疮', '皮肤油腻', '先天性虹膜缺乏', '光感性皮肤损害', '溃疡', '寒凝下焦', '鼻塞', '地图样骨缺损', '劳动后气急',
        '剥夺性弱视', '药疹', '血管萎缩性白斑', '大疱（含脓性液体）', '胸骨后疼痛', '下腹痛', '回吸性涕血', '尿液混浊',
        '皮肤干枯', '嗜酒', '高通气', '颅骨连续性中断', '小管毒性病变', '胸膈间烧灼嘈杂感', '女性小腹疼痛', '溃疡疼痛', '衰弱',
        '经闭不行', '慢性房颤', '吞咽疼痛', '夹层血肿', '皮肤痣', '烧伤创面甜腥气味的粘稠分泌物', '死血痛', '忧郁', '虚脱',
        '小肠危象', '颈部肌肉肿胀变硬', '灰白色结节', '肺外症状', '高氨血症', '血性恶露', '湿痒生疮', '弥漫性鼓音', '肝静脉病变',
        '直肠危象', '血管搏动或波形的改变', '幽门管狭窄', '维生素缺乏', '髋关节痛', '胎动频繁', '静脉栓塞', '热结节',
        '颈髓硬膜外病变', '毛窍闭塞', '厌奶', '凝血障碍', '血偏酸', '溃疡龛影', '维生素B族缺乏', '血管增生', '软组织肿胀',
        '尿酸代谢亢进', '舌位于口腔底不能外伸', '恶寒无汗较严重', '全身皮肤粗厚', '蜘蛛蛊', '场所恐惧', '输尿管间脊肥大',
        '行为及情绪异常', '骨髓的发育异常', '软组织感染', '室上性心律失常', '绝经', '尿黑酸', '指鼻不准', '网眼样痴呆', '自主神经反射',
        '牵涉痛', '骨代谢减低', '静脉回流障碍', '黏膜出现出血点', '尿暗黑色', '泌尿道狭窄', '绞痛', '失盐', '假孕', '迷走神经张力增高',
        '坠痛', '细胞酶活性异常', '皮肤出血斑', '胃肠道症状', '巨痕症', '耳廓腹侧面局限性囊肿', '糖类皮质激素分泌过多', '成年后的容貌仍似儿童',
        '骶尾部窦道形成', '血缺氧', '震水音', '上腹部包块', '糖激素依赖', '舌体大且表面有沟纹', '自发性骨折', '多发性结节',
        '机械地重复周围人的言语或行为', '髋外侧可见皮下瘀血斑', '啰音', '心瓣膜病变', '内出血', '耳垂里有硬疙瘩', '肺动脉闭锁',
        '第二性征改变', '慢性胃痛', '舌骨区有肿胀压痛', '脱肛', '新生儿发绀', '向心性肥胖', '红细胞呈钱串状', '乳头侵蚀', '无痛性硬实结节',
        '言语功能的部分丧失', '乳头肌断裂', '全血细胞减少', '黄色结节', '胸壁塌陷', '小胆管扭曲', '输尿管疼痛', '情绪性多汗症',
        '高凝状态', '无用感', '情绪性癌症', '儿童期过度生长', '蜘蛛指', '脱症', '先天性无虹膜', '颈部不稳感', '凹陷瘢痕',
        '充血', '毛发呈脱发祥', '性交疼痛', '全身代谢低下', '津亏血燥', '细菌的混合感染', '近迫性心肌梗塞', '冷结节', '下腹部包块',
        '斑丘疹', '儿童反复骨折', '血糖升高', '耳廓痛', '反复感染', '吸气时上气道陷闭', '坐骨大小孔区出现压痛', '食管腔梗阻',
        '过度换气引起晕厥', '血瘀体质', '盲肠阿米巴肉芽肿', '气过水声', '回盲瓣功能不全', '髋部酸胀不适', '凉结节', '上行性皮肤麻木',
        '阴虚体质', '锥体外系损害', '脓肿', '生殖泌尿道危象', '脾胃不和', '隐性水肿', '脉沉缓或沉细', '交替脉', '粘液性水肿面容',
        '皮肤丰满度丧失', '食道病变', '胸骨后烧灼样痛', '颈部淋巴结肿大', '红细胞分布宽度偏高', '盗汗', '后发性遗忘',
        '肺源性呼吸困难', '人格改变', '尿胆原增加', '真性菌尿', '肠蠕动减慢', '下腹压痛', '食欲异常', '电机械分离现象', '胃危象',
        '耳廓耳道撕裂伤', '舌根部脓肿', '低热消疲', '骨骼变形缩短', '肾上腺皮质激素不足', '拇指三节', '梅毒恐怖', '掌跖角化过度',
        '年轻人的眼袋', '钙沉积', '躯体依赖性', '皮质功能减退', '胸膜钙化', '血管硬化', '输乳管阻塞', '重度痛', '骨髓象改变',
        '免疫缺陷', '剧痒的疣状结节', '口、眼、生殖器损害', '耳硬化症', '胃扩张', '早孕反应重', '紧张', '溲黄', '逸搏出现', '过度通气',
        '胆汁返流', '病理性Q波', '肠蠕动减少', '静脉内持续性血流', '室间隔缺损', '弥漫性系膜硬化', '血管性痴呆', '儿童行为孤僻',
        '反复肺炎', '无痛性尿血', '躁郁样', '颈动脉搏动减弱或消失', '股骨近侧端变宽', '继发感染', '吐泡沫痰', '压迫瘘口试验',
        '静脉出血', '耳蜗性耳聋', '第一心音亢进', '血运障碍', '糖耐量降低', '难入睡或易惊醒', '烫伤后汗腺受损', '情绪低落',
        '肝肾综合征', '乳汁淤积', '丘疹', '食管重复', '肝细胞脂肪性变', '心率增快', '继发性不孕', '气逆', '囊肿样改变',
        '脊柱的成角畸形', '肝窦扩张', '骨及软组织肥大', '网状色素沉着斑', '软骨内骨化', '环咽部运动障碍', '胃纳减退', '经期肿胀',
        '酒精性震颤', '扁平型骨盆', '肺动脉瓣狭窄杂音', '凝血因子功能的障碍', '酒后便血', '剧烈疼痛', '溃疡分泌物恶臭',
        '腹围增大', '腹股沟区可复性肿块', '脓毒性血栓', '胸膜转移', '膈肌缺损', '窦道相', '呼吸浅慢', '单项ALT升高', '消耗性体重下降',
        '烧伤后恶心与呕吐', '灾难反应', '红细胞畸形', '脉数', '酒精中毒性偏执状态', '跨阈步态', '乳糜泻', '腹股沟疼痛', '脂肪代谢障碍',
        '血管性水肿', '血管过敏性炎症', '泌乳障碍', '心跳很乱', '慢性溃疡', '热痉挛', '慢性盆腔痛', '排尿不畅', '突发性绞痛', '行走呈大步态',
        '吐弄舌', '肝转移', '蝶鞍变形', '压力和体位性多汗', '孕晚期腹痛', '脐突', '低氧血症', '食管左壁形成压足跡', '胃容纳性减弱',
        '营养障碍', '颞部疼痛', '髂窝部疼痛', '皮肤浸润', '颈椎骨折脱位', '耳内流脓', '血离脉络', '休克性神经受累', '懒胆囊',
        '神经衰弱综合征', '回声阴影', '泌尿生殖窦', '脐周肿胀', '啤酒肚', '凹陷性疤痕', '腋区疼痛', '仰颈时吞咽困难',
        '幽门肌肥大', '剧痛', '经常说梦话', '门静脉积气', '烧灼性疼痛', '行走踩棉花感', '类癌综合征', '纤维渗出物',
        '高雄激素血症', '组织细胞增生', '尿意窘迫', '子宫高度低于妊娠周数', '耳孔处肿物', '瘤块压迫', '醛固酮分泌增多',
        '第三心音奔马律', '舌口及咽部烧灼感', '过敏性皮炎', '胎盘大', '脓性分泌物', '皮肤钙沉着', '静脉血栓', '发作后精神障碍',
        '绝望感', '鼻痒', '颈部囊性病变', '肌肉萎缩', '胀感', '粪便脓血', '心肌细胞的浊肿', '假临产', '舌背中后部黑色丛毛',
        '颈交感链受累', '酒精性幻觉症', '入球小动脉玻璃样变', '先天性少白头', '乳房巨大', '躯体形式疼痛障碍', '骨骺提前闭合', '粪便量多',
        '幽门瘢痕性狭窄', '腹肌严重发育不良', '肺弥散功能障碍', '肺受累', '心电图异常', '椎管大小变化', '脉搏加速',
        '溃疡外观呈火山口样', '颈短', '咳血痰', '慌张步态', '肝细胞索支架塌陷', '反复出血', '过早丧失咀嚼功能', '胸腔出口综合征', '收缩期杂音',
    ]

    symptom_file = 'symptom.json'

    for symptom in symptom_lists:
        cql = """match (n:症状) where n.名称='%s' return labels(n)""" % symptom
        print(graph.run(cql).data())  # [{'labels(n)'}，{}]

        labels_dict = graph.run(cql).data()  # [{'labels(n)'},{}]
        label_list = []

        for label in labels_dict:
            labels = label['labels(n)']
            label_list += labels
            print(label_list)

        label_list = list(set(label_list))
        # 找所有的节点和关系
        cql = """match (n:症状)-[r]-(m) where n.名称='%s' return n.名称,r,id(m)""" % symptom
        node_info = graph.run(cql).data()
        print(node_info)

        js_nodes = json.dumps(node_info, ensure_ascii=False)

        with open('症状节点信息.json', 'wb') as ff:
            ff.write(js_nodes.encode('utf-8'))

        with open('症状节点信息.json', 'r', encoding='utf-8') as f:
            content = f.read()
            nodes = json.loads(content)  # list
            print(len(nodes))
        ready_node = []
        for node in nodes:
            if node not in ready_node:
                ready_node.append(node)
        print(len(ready_node))

        # 删除原有节点，新建节点，并创建关系
        delete = """match (n:症状)<-[r]-(m) where n.名称='%s' delete r""" % symptom  # TODO 若没有关系这条语句删除不了节点

        print(delete)
        graph.run(delete)
        delete2 = """match (n:症状)<-[r]-(m) where n.名称='%s' delete n""" % symptom
        print(delete2)
        graph.run(delete2)

        node_add = """create (n:"""
        for lab in label_list:
            node_add += lab
            node_add += ':'
        node_add = node_add[:-1] + "{名称:'%s'})" % symptom
        graph.run(node_add)
        print(node_add)

        print(len(ready_node))
        n = 0
        for node in ready_node:
            query1 = "match(p:症状{名称:'%s'}),(q) where id(q) = %s merge (p)<-[rel:%s{名称:'%s'}]-(q)" % (
                symptom, node['id(m)'], node['r'].get('名称', '未定义'), node['r'].get('名称', '未定义'))
            print(query1)
            n += 1
            # print(n)
            graph.run(query1)

        print(n)

#整合重名药品
def merge_drug():
    #先读取重名药品
    with open('./same_drug.txt','r',encoding='utf-8') as file:
        content = file.readlines()
        print(len(content))

        for drug in content:
            print(drug[:-1])
            cql = """match (n:药品) where n.名称='%s' return n.名称 as 名称, id(n) as id"""%drug[:-1]
            print(cql)
            res = graph.run(cql)   #[{},{}]
            #取出其中id
            id_list = []
            for dict in res:
                id = dict.get('id')
                if id not in id_list:
                    id_list.append(id)
            #取出要删除的id
            ids = id_list[:-1]
            print(ids)
            for id in ids:
                cql = """match (n:药品)-[r]-(m) where id(n)=%s delete n,r"""%id
                print(cql)
                graph.run(cql)

    print('删除完毕')


if __name__ == '__main__':
    merge_location("头","头部","头")
    merge_location("手", "手部", "手")
    merge_location("鼻", "鼻部", "鼻")
    merge_location("足", "足部", "足")
    merge_location("面", "面部", "面")
    merge_location("眼", "眼部", "眼")

    merge_location('耳','耳部','耳')  #待完成
    merge_symptom()
    merge_drug()


