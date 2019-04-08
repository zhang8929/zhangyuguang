import re
import json
import pandas as pd
with open('./buyunbuyu_500wen.txt','r') as file:
    content = file.readlines()
    # print(len(content))

    result = []
    # id=1
    for qa in content:
        tmp = {}
        q = re.match('\d.*\?', qa)
        q = q.group()
        s = re.search('(\d*\.)', q)
        del_s = s.group()
        key = q.replace(del_s,'')
        tmp['question']=key
        tmp['answer']=qa.replace(q,'')[:-1]
        # tmp['id']=id
        # id += 1
        result.append(tmp)

print(result)
data_list=[]
column = ['question','answer']
for dict in result:
    tt = []
    # tt.append(dict['id'])
    tt.append(dict['question'])
    tt.append(dict['answer'])
    data_list.append(tt)

print(data_list)

test=pd.DataFrame(columns=column,data=data_list)
print(test)
test.to_csv('/Users/zhangyuan/work/qa.csv',encoding='utf_8_sig')
# ready_data = json.dumps(result,ensure_ascii=False)
# with open('/Users/zhangyuan/work/buyunbuyu.json','w') as file:
#     file.write(ready_data)

