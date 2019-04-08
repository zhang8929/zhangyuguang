import json,re

# 原数据中complication字段未入库
with open(r'D:\nlp\医疗\爬虫数据\快速问医生\kswys.json','r',encoding='utf-8') as file:
    content = file.read()
    content = json.loads(content)['RECORDS']  #[{},{},{}]
    print(type(content))
    print(len(content))

ready_list = []
for dict in content:
    tmp_dict = {}
    tmp_dict['名称'] = dict.get('title','')
    tmp_dict['宜吃'] = dict.get('suitable','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['忌吃'] = dict.get('taboo','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['饮食保健'] = dict.get('diet','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['病因'] = dict.get('pathogeny','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['病症详述'] = dict.get('symptom','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['检查内容详述'] = dict.get('examine','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['鉴别详述'] = dict.get('identify','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['预防详述'] = dict.get('prevent','暂无数据').replace('    ','').replace("'",'"').strip()
    tmp_dict['治疗方法详述'] = dict.get('cures','暂无数据').replace('    ','').replace("'",'"').strip()
    jc = dict.get('examine','暂无数据')
    jc_str = re.findall(r"检查项目：(.*?) ", jc)
    if jc_str:
        jc_list = re.findall(r"检查项目：(.*?) ", jc)[0].strip().split('、')
        tmp_dict['检查项目'] = re.findall(r"检查项目：(.*?) ", jc)[0].strip().split('、')

    if tmp_dict not in ready_list:
        ready_list.append(tmp_dict)

print(len(ready_list))
ready_data = json.dumps(ready_list,ensure_ascii=False)
print(len(ready_data))

with open ('kswys_1.json','wb') as file:
    file.write(ready_data.encode('utf-8'))


with open('kswys_1.json','r',encoding='utf-8') as file:
    content = file.read()
    content = json.loads(content)   #[{},{},{}]
    print(type(content))
    print(len(content))



