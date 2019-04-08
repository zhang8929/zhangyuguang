import requests
import json
from lxml import etree

class Kang99():
       def __init__(self):
           self.url='https://www.991kang.com/awyh/articleIndex/getAnalysisByPage/?=pageIndex=2&limit=3000&departId='
           self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
       def fist_url(self):

          sep= requests.get(self.url,headers=self.headers)
          seps=(sep.content).decode()
          s_list= json.loads(seps)
          list_data=s_list["data"]
          for i in list_data:
              dict1 = {}

              dict1["question"]=i['ucontent']
              if dict1["question"]=='':
                  continue

              dict1["answer"]=i['acontent']
              joan=json.dumps(dict1,ensure_ascii=False)
              print(joan)
              with open('991.json','a',encoding='utf-8')as f:
                    f.write(joan+','+'\n')

kang=Kang99()
kang.fist_url()

