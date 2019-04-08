# import re,json
# with open('/Users/zhangyuan/Documents/files/menzhen_jk.txt','r') as file:
#     content = file.readlines()
#     print(len(content))
#
# res_list = []
# id = 1
# for row in content:
#     tmp={}
#     # print(row)
#     res = re.search('(.*疾病概述.*)(.*病因.*)(.*临床表现.*)(.*治疗原则.*)(.*###健康教育.*)', row)
#     name = re.search('(.*)\(一\)疾病概述.*',row)
#     if name is None or res is None:
#         print('--')
#     else:
#         title = name.group(1)
#         tmp['名称'] = title
#         tmp['疾病概述'] = res.group(1)
#         tmp['病因'] = res.group(2)
#         tmp['临床表现'] = res.group(3)
#         tmp['治疗原则'] = res.group(4)
#         tmp['健康教育'] = res.group(5)
#         tmp['id'] = id
#         id += 1
#         # res_list.append(tmp)
#     #     # res_list.append(',\n')
#         with open('/Users/zhangyuan/Documents/files/menzhen_jk_1.json','a')as f:
#             f.write(json.dumps(tmp,ensure_ascii=False))
#             f.write(',\n')

# json_list = json.dumps(res_list,ensure_ascii=False)
# with open('/Users/zhangyuan/Documents/files/menzhen_jk.json','w') as ff:
#     ff.write(json_list)

import pandas as pd
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/PGC?charset=utf8mb4'
conn= create_engine(SQLALCHEMY_DATABASE_URI)

df = pd.read_json("/Users/zhangyuan/Documents/files/menzhen_jk.json")
df.to_sql("menzhen_jk", con=conn,if_exists='replace',index=False, chunksize=100)