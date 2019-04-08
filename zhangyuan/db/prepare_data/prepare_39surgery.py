import json
import json,re

with open(r'D:\nlp\医疗\爬虫数据\三九\39手术.json',encoding='utf-8') as file:
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
        # print(dict)
        tmp_dict = {}
        tmp_dict['名称'] = dict.get('title','').strip()
        tmp_dict['别名'] = dict.get('alias')[4:-1].split(',')
        tmp_dict['手术方式']  =dict.get('label','暂无数据')
        tmp_dict['手术简介'] = dict.get('introdce','暂无数据')
        basic_information = dict['basic_information']
        basic_information = json.loads(basic_information)   #[{},{}]
        print(basic_information)
        for x in basic_information:  #{}

            print(list(x.keys())[0])
            if list(x.keys())[0] == '相关疾病：':
                continue
            tmp_dict[list(x.keys())[0]] = x[list(x.keys())[0]]
        else_informatin = dict['else_information']
        else_informatin = json.loads(else_informatin)
        for x in else_informatin:
            if '术前' in list(x.keys())[0]:
                key = '术前准备'
            if '适应症' in list(x.keys())[0]:
                key = '手术适应症'
            if '术后' in list(x.keys())[0]:
                key = '手术术后'
            if '不适宜人群' in list(x.keys())[0]:
                key = '不适宜人群'
            if '手术过程' in list(x.keys())[0]:
                key = '手术过程'
            if '相关疾病' in list(x.keys())[0]:
                key = '相关疾病'
            if '相关症状' in list(x.keys())[0]:
                key = '相关症状'
            if key=='相关疾病' or key=='相关症状':
                tmp_dict[key] = x.get(list(x.keys())[0],['暂无数据']).strip().split('  ')
            else:
                tmp_dict[key] = x.get(list(x.keys())[0].strip(),'暂无数据')


        if dict not in ready_list:
            ready_list.append(tmp_dict)

    ready_data = json.dumps(ready_list,ensure_ascii=False)
    with open('39_surgery.json','wb') as file:
        file.write(ready_data.encode('utf-8'))



