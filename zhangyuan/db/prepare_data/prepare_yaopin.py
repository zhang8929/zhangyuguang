import json

def prepare_tmpp(file1,file2):
    """
    统一处理药品文件
    :param file1: 读取的来源文件
    :param file2: 写入的目标文件
    :return: json
    """
    with open (file1, 'r', encoding='utf-8') as file:
        content = file.read()  #str
        json_data = json.loads(content,encoding='utf-8')['RECORDS']
        # print(type(json_data))
        list1 = []
        for dict in json_data:
            # print(dict['title'])
            tmp={}
            tmp['名称'] = dict['title']  #确保都有  无需默认值
            print(tmp['名称'])
            particular_list = json.loads(dict['particulars'])
            for dicts in particular_list:
                tmp[list(dicts.keys())[0]] = list(dicts.values())[0]




            basic_information = dict['basic_information']
            if basic_information is '':
                new_list =[]
            else:
                basic_list = json.loads(dict['basic_information'])
                print(type(basic_list))
                print(len(basic_list))
                for basic in basic_list:
                    new_list = []
                    if basic[0:4] == '相关疾病':
                        jb_list = basic[6:].strip().split(',')
                        print(jb_list)
                        for jb in jb_list:
                            jb = jb.strip()
                            if '...' not in jb[-3:]:
                                 new_list.append(jb)

                        print(new_list)

            tmp['适用疾病'] = new_list

            # print(type(json.loads(dict['specification'])))
            specification_list = json.loads(dict['specification'])

            for dict in specification_list:
                tmp[list(dict.keys())[0]] = list(dict.values())[0]
            tmp['特殊人群用药'] = tmp.get('儿童用药','')+tmp.get('老人用药','')+tmp.get('孕妇及哺乳期妇女用药','')

            # if '卫食健字' in tmp['批准文号'] or '国食健字' in tmp['批准文号']:  #数据一致则跳过，没有就添加，冲突则人工
            #     tmp['药品类别'] = '保健食品'
            # elif '国药准字H' in tmp['批准文号']:
            #     print('if H')
            #     tmp['药品类别'] = '化学药品'
            # elif '国药准字Z' in tmp['批准文号']:
            #     print('if z')
            #
            #     tmp['药品类别'] = '中成药'
            # elif '国药准字S' in tmp['批准文号']:
            #     tmp['药品类别'] = '生物制品'
            # elif '国药准字B' in tmp['批准文号']:
            #     tmp['药品类别'] = '保健药品'
            # elif '国药准字T' in tmp['批准文号']:
            #     tmp['药品类别'] = '体外化学诊断试剂'
            # elif '国药准字F' in tmp['批准文号']:
            #     tmp['药品类别'] = '药用辅料'
            # elif '国药准字J' in tmp['批准文号']:
            #     tmp['药品类别'] = '进口分包装药品'
            # elif '注册账号H' in tmp['批准文号']:
            #     tmp['药品类别'] = '进口化学药品'
            # else:
            #     print('else'+tmp['批准文号'])
            #     tmp['药品类别'] = '暂无数据'  #保健品无该字段


            if tmp not in list1:
                list1.append(tmp)
        #
        print(len(list1))
        with open(file2,'w',encoding='utf-8') as ffile:
            ffile.write(json.dumps(list1,ensure_ascii=False))



if __name__ == '__main__':
    # prepare_tmpp(r'D:\nlp\医疗\爬虫数据\快速问医生\kswys_yp.json','./kswys_yp_ready.json')  #2019-2-10日录入，共12870 条数据。 无英文名称，无处方药，无适用症,无特殊人群用药
    prepare_tmpp(r'C:\Users\zhang\Desktop\new6.json','./new6_ready.json')   #62533 条数据

