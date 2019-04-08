import json
import json,re

with open(r'D:\nlp\医疗\爬虫数据\三九\39检查_1.json',encoding='utf-8') as file:
    # content = file.read()
    content = file.read()
    print((type(content)))
    # for i in content:
    #     print(i)
    content = json.loads(content)['RECORDS']
    print(type(content))

    # print(content[0])
    ready_list = []
    for dict in content:
        print(dict)
        tmp_dict = {}
        tmp_dict['名称'] = dict.get('title','').strip()
        tmp_dict['别名'] = dict.get('alias')[4:-1].split(',')
        tmp_dict['检查项目简介'] = dict.get('introdce','暂无数据')
        basic_information = dict['basic_information']
        basic_information = json.loads(basic_information)   #[{},{}]
        # print(basic_information)
        for x in basic_information:  #{}

            # print(list(x.keys())[0])
            if list(x.keys())[0] == '相关疾病：' or list(x.keys())[0] == '相关症状：':
                continue
            if list(x.keys())[0] == '检查部位：':
                tmp_dict['检查部位_list'] = x.get(list(x.keys())[0], ['暂无数据']).strip().split(' ')
            if list(x.keys())[0] == '科室：':
                tmp_dict[list(x.keys())[0]] = x.get(list(x.keys())[0], ['暂无数据']).strip().split('  ')
            # if list(x.keys())[0] == '空腹检查：':
            #     sfkf = dict.get('空腹检查：','暂无数据')
            #     # print('====')
            #     print(sfkf)
            #     if '是' in sfkf:
            #         print('----')
            #         tmp_dict['是否空腹'] = True
            #     if '否' in sfkf:
            #         tmp_dict['是否空腹'] = False

            else:
                tmp_dict[list(x.keys())[0]] = x[list(x.keys())[0]]
        else_informatin = dict['else_information']
        else_informatin = json.loads(else_informatin)
        for x in else_informatin:
            if '注意事项' in list(x.keys())[0]:
                key = '注意事项'
            if '相关疾病' in list(x.keys())[0]:
                key = '相关疾病'
            if '相关症状' in list(x.keys())[0]:
                key = '相关症状'
            if '检查作用' in list(x.keys())[0]:
                key = '临床意义'
            if '检查过程' in list(x.keys())[0]:
                key = '检查过程'
            if key=='相关疾病' or key=='相关症状':
                tmp_dict[key] = x.get(list(x.keys())[0],['暂无数据']).strip().split(' ')
            else:
                tmp_dict[key] = x.get(list(x.keys())[0].strip(),'暂无数据')


        if dict not in ready_list:
            ready_list.append(tmp_dict)
    print(len(ready_list))
    ready_data = json.dumps(ready_list,ensure_ascii=False)
    with open('39_检查.json','wb') as file:
        file.write(ready_data.encode('utf-8'))



