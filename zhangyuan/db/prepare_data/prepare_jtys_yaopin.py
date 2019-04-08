import json,re


def prepare_tmpp(file1,file2):
    """
    统一处理药品文件
    :param file1: 读取的来源文件
    :param file2: 写入的目标文件
    :return: json
    """
    with open (file1, 'r', encoding='utf-8') as file:
        content = file.readlines()  #str
        # print(type(json_data))
        print(len(content))
        list1 = []
        name_list = []
        for dict in content[1:-1]:
            dict = json.loads(dict[:-2])
            tmp={}
            tmp['名称'] = dict.get('title','暂无数据').strip()
            # print(tmp['名称'])
            tmp['英文名称'] = dict.get('title','暂无数据')
            tmp['批准文号'] = dict.get('批准文号：','暂无数据')
            # tmp['药品通用名称'] = dict.get('title','暂无数据')
            name = dict.get('title').strip()
            re_name = re.findall(r'\(.*?\)',name)
            # print(re_name)
            if len(re_name)==0:
                tmp['药品通用名称'] = tmp['名称']
            else:
                tmp['药品通用名称'] = re_name[0][1:-1]
            # print(re_name)
            tmp['制药公司'] = dict.get('生产企业：','暂无数据')
            tmp['处方药'] = dict.get('title','暂无数据')
            tmp['用法用量'] = dict.get('【用法用量】','暂无数据')
            tmp['适用疾病'] = dict.get('治疗疾病：','暂无数据').strip().split(' ')
            tmp['适用症状'] = dict.get('适用症状','暂无数据')
            tmp['适用症描述'] = dict.get('功效主治：','暂无数据')
            tmp['特殊人群用药'] = dict.get('特殊人群用药','暂无数据')
            tmp['成分'] = dict.get('【成分】','暂无数据')
            tmp['禁忌'] = dict.get('禁忌','暂无数据')
            tmp['注意事项'] = dict.get('【注意事项】','暂无数据')
            tmp['不良反应'] = dict.get('副作用','暂无数据')
            tmp['有效期'] = dict.get('有效期','暂无数据')
            tmp['药物相互作用'] = dict.get('【相互作用】','暂无数据')
            tmp['图片'] = dict.get('图片','暂无数据')
            tmp['url'] = dict.get('url','暂无数据')

        #     particular_list = json.loads(dict['particulars'])
        #     for dicts in particular_list:
        #         tmp[list(dicts.keys())[0]] = list(dicts.values())[0]
        #
        #
        #
        #
        #     basic_information = dict['basic_information']
        #     if basic_information is '':
        #         new_list =[]
        #     else:
        #         basic_list = json.loads(dict['basic_information'])
        #         print(type(basic_list))
        #         print(len(basic_list))
        #         for basic in basic_list:
        #             new_list = []
        #             if basic[0:4] == '相关疾病':
        #                 jb_list = basic[6:].strip().split(',')
        #                 print(jb_list)
        #                 for jb in jb_list:
        #                     jb = jb.strip()
        #                     if '...' not in jb[-3:]:
        #                          new_list.append(jb)
        #
        #                 print(new_list)
        #
        #     tmp['适用疾病'] = new_list
        #
        #     # print(type(json.loads(dict['specification'])))
        #     specification_list = json.loads(dict['specification'])
        #
        #     for dict in specification_list:
        #         tmp[list(dict.keys())[0]] = list(dict.values())[0]
        #     tmp['特殊人群用药'] = tmp.get('儿童用药','')+tmp.get('老人用药','')+tmp.get('孕妇及哺乳期妇女用药','')
        #
            if '卫食健字' in tmp['批准文号'] or '国食健字' in tmp['批准文号']:  #数据一致则跳过，没有就添加，冲突则人工
                tmp['药品类别'] = '保健食品'
            elif '国药准字H' in tmp['批准文号']:
                # print('if H')
                tmp['药品类别'] = '化学药品'
            elif '国药准字Z' in tmp['批准文号']:
                # print('if z')

                tmp['药品类别'] = '中成药'
            elif '国药准字S' in tmp['批准文号']:
                tmp['药品类别'] = '生物制品'
            elif '国药准字B' in tmp['批准文号']:
                tmp['药品类别'] = '保健药品'
            elif '国药准字T' in tmp['批准文号']:
                tmp['药品类别'] = '体外化学诊断试剂'
            elif '国药准字F' in tmp['批准文号']:
                tmp['药品类别'] = '药用辅料'
            elif '国药准字J' in tmp['批准文号']:
                tmp['药品类别'] = '进口分包装药品'
            elif '注册账号H' or '注册证号H' in tmp['批准文号']:
                tmp['药品类别'] = '进口化学药品'
            elif '注册账号S' or '注册证号S' in tmp['批准文号']:
                tmp['药品类别'] = '进口生物制品'
            else:
                # print('else'+tmp['批准文号'])
                tmp['药品类别'] = '暂无数据'  #保健品无该字段
        #
        #
            if tmp not in list1:
                list1.append(tmp)
        # print(name_list)
        # with open('/Users/zhangyuan/work/爬虫数据/yaopinname.txt','r',encoding='utf-8') as fff:
        #     name_lists = fff.readlines()
        #     for name in name_list:
        #         if name not in name_lists:
        #             print(name)
        print(len(list1))
        with open(file2,'w',encoding='utf-8') as ffile:
            ffile.write(json.dumps(list1,ensure_ascii=False))



if __name__ == '__main__':
    prepare_tmpp('/Users/zhangyuan/work/爬虫数据/家庭医生/jtys_5.json','/Users/zhangyuan/work/爬虫数据/家庭医生/jtys_ready_5.json')  #47630 条数据
    # prepare_tmpp(r'C:\Users\zhang\Desktop\new6.json','./new6_ready.json')   #62533 条数据

