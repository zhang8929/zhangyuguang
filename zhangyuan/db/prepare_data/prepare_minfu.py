import json

def prepare_tmpp(file1,file2):
    """
    统一处理药品文件
    :param file1: 读取的来源文件
    :param file2: 写入的目标文件
    :return: json
    """
    with open (file1, 'r', encoding='utf-8') as file:
        content = file.readlines()
        # print(content[0])
        # print(content[1])
        list1 = []
        for dict in content:
            # print(dict[:-2])
            dict=dict[:-2]
            dict = json.loads(dict,encoding='utf-8')  #dict
            tmp={}
            tmp['名称'] = dict['标题']  #确保都有  无需默认值
            # print(tmp['名称'])
            tmp['url'] = dict['url']
            tmp['适用疾病'] = dict['适用疾病'].strip().replace(' ',',').split(',')
            # print(tmp['相关疾病'])
            # tmp['药品通用名称'] = dict['说明书']
            for x in dict['说明书']:
                tmp[list(x.keys())[0]] = list(x.values())[0].strip()
            # print(tmp)


            # # print(type(json.loads(dict['specification'])))
            # specification_list = json.loads(dict['specification'])
            #
            # for dict in specification_list:
            #     tmp[list(dict.keys())[0]] = list(dict.values())[0]
            # tmp['特殊人群用药'] = tmp.get('儿童用药','')+tmp.get('老人用药','')+tmp.get('孕妇及哺乳期妇女用药','')

            if '卫食健字' in tmp.get('批准文号','暂无数据') or '国食健字' in tmp.get('批准文号','暂无数据'):  #数据一致则跳过，没有就添加，冲突则人工
                tmp['药品类别'] = '保健食品'
            elif '国药准字H' in tmp.get('批准文号','暂无数据'):
                # print('if H')
                tmp['药品类别'] = '化学药品'
            elif '国药准字Z' or '国药准字z' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '中成药'
            elif '国药准字S' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '生物制品'
            elif '国药准字B' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '保健药品'
            elif '国药准字T' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '体外化学诊断试剂'
            elif '国药准字F' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '药用辅料'
            elif '国药准字J' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '进口分包装药品'
            elif '注册账号H' in tmp.get('批准文号','暂无数据'):
                tmp['药品类别'] = '进口化学药品'
            else:
                print('else'+tmp.get('批准文号','暂无数据'))
                tmp['药品类别'] = '暂无数据'  #保健品无该字段


            if tmp not in list1:
                list1.append(tmp)
        #
        print(len(list1))
        with open(file2,'w',encoding='utf-8') as ffile:
            ffile.write(json.dumps(list1,ensure_ascii=False))



if __name__ == '__main__':
    # prepare_tmpp(r'D:\nlp\医疗\爬虫数据\快速问医生\kswys_yp.json','./kswys_yp_ready.json')  #2019-2-10日录入，共12870 条数据。 无英文名称，无处方药，无适用症,无特殊人群用药
    prepare_tmpp(r'D:\nlp\医疗\爬虫数据\minfu.json','./minfu_ready.json')  #663条数据

