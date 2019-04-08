import json,re

with open(r'D:\nlp\医疗\爬虫数据\寻医问药\xunyijiancha.json',encoding='utf-8') as file:
    # content = file.read()
    content = file.read()
    print((type(content)))
    # for i in content:
    #     print(i)
    content = json.loads(content)
    # print(type(content))

    ready_list = []
    for dict in content:
        tmp_dict = {}
        tmp_dict['名称'] = dict.get('检查项目', '').replace("'",'"').strip()
        tmp_dict['注意事项'] = dict.get('注意事项', '暂无数据').replace('    ', '').replace("'", '"').strip()
        if dict.get('相关检查') is None:
            tmp_dict['相关检查'] = ['暂无数据']
        else:
            tmp_dict['相关检查'] = dict.get('相关检查', ['暂无数据'])

        if dict.get('科室') is None:
            tmp_dict['科室'] = ['暂无数据']
        else:
            tmp_dict['科室'] = dict.get('科室', ['暂无数据'])

        tmp_dict['相关症状'] = dict.get('相关症状', ['暂无数据'])
        tmp_dict['检查过程'] = dict.get('检查过程', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['参考价格'] = dict.get('参考价格', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['适用性别'] = dict.get('适用性别', '暂无数据').replace('    ', '').replace("'", '"').strip()
        sfkf = dict.get('是否空腹', '暂无数据').replace('    ', '').replace("'", '"').strip()
        if sfkf == '空腹':
            tmp_dict['是否空腹'] = True
        if sfkf == '非空腹':
            tmp_dict['是否空腹'] = False
        jcfl = dict.get('检查分类')
        if jcfl is None:
            tmp_dict['检查分类'] = '暂无数据'
        else:
            tmp_dict['检查分类'] = dict.get('检查分类', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['不适宜人群'] = dict.get('不适宜人群', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['检查项目简介'] = dict.get('介绍', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['相关疾病'] = dict.get('相关疾病', ['暂无数据'])
        tmp_dict['不良反应与风险'] = dict.get('不良反应与风险', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['临床意义'] = dict.get('临床意义', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['温馨提示'] = dict.get('温馨提示', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['正常值'] = dict.get('正常值', '暂无数据').replace('    ', '').replace("'", '"').strip()
        tmp_dict['url'] = dict.get('url', '暂无数据').replace('    ', '').replace("'", '"').strip()


        if tmp_dict not in ready_list:
            ready_list.append(tmp_dict)

print(len(ready_list))
ready_data = json.dumps(ready_list,ensure_ascii=False)
print(len(ready_data))

with open ('xywy_jc_1.json','wb') as file:
    file.write(ready_data.encode('utf-8'))


with open('xywy_jc_1.json','r',encoding='utf-8') as file:
    content = file.read()
    content = json.loads(content)   #[{},{},{}]
    print(type(content))
    print(len(content))
