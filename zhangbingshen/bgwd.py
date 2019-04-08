import json
import requests
from lxml import etree
import re


class Bgwd():
    def __init__(self):

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        'Cookie':'tracker_u=nr-wenda; vid=U4A3B1545899244841; uid=U9D1F1545899244841; LiveWSDQT22380516=08c909140cf24d03a3c35c32f11a28e3; LiveWSDQT22380516sessionid=08c909140cf24d03a3c35c32f11a28e3; NDQT22380516fistvisitetime=1545899246161; '
        'NDQT22380516visitecounts=1; UM_distinctid=167eec6828782-0e950d5d4d2727-51422e1f-e1000-167eec68288330; NDQT22380516IP=%7C121.69.132.42%7C; tcpos=m--0--0--0--0--0--0--0--0; CNZZDATA1263247556=1736488214-1545894713-%7C1545900293; NDQT22380516lastvisitetime=1545903887319; NDQT22380516visitepages=13; NDQT22380516lastinvite=1545903927913; NDQT22380516LR_check_data=4%7C1545903928044%7C%7C%7C'}
    def frist_url(self):
          try:
                for z in range(0,6200,20):
                    print(z)
                    url_firt="http://bgwd.360haoyao.com/qa/column/toMore?id=&start={}&length=20".format(20)
                    sep=requests.get(url_firt,headers=self.headers)
                    html=sep.text
                    print(html)
                    print(type(html))
                    bi=re.findall('/qa/detail/\d+.html',html)
                    print(bi)
                    for i in bi :
                        urls='http://bgwd.360haoyao.com'+i
                        sep=requests.get(urls,headers=self.headers)
                        html=etree.HTML(sep.content)
                        dict1={}
                        dict1["url"]=urls
                        print(dict1["url"])
                        dict1['question']=html.xpath('//div[@class="qaDetail"]/div/text()')[0]

                        m= html.xpath('//dl[@class="dl_q clearfix"]/dd/p[1]/text()')
                        if len(m)==0:
                            dict1['describe']='meiyou '
                            print( dict1['describe'])
                        dict1['describe']=' '
                        dict1['answer'] = html.xpath('//dl[@class="dl_a clearfix"]/dd/text()')[0]
                        print(dict1)
                        json_dict=json.dumps(dict1,ensure_ascii=False)
                        with open('gbwd.josn','a',encoding='utf-8')as f:
                            f.write(json_dict+','+'\n')
          except:
              pass


    def run(self):
        self.frist_url()
        pass

bgwd=Bgwd()
bgwd.run()