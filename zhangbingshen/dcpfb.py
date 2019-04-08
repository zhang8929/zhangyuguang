import requests
from lxml import etree
import json,re
import time
class  Dcpfb(object):
    '''达成皮肤站'''
    def __init__(self):
        self.url='http://www.dcpfb.com/ask/browser-lm-3-1.html'
        self.headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                      }
    def data_url(self,next_url):

        try:
            solve = requests.get(next_url,headers=self.headers)
            print(solve)

            html = etree.HTML(solve.content)
            list_url_solve = html.xpath("//div[@class='know_box']/div/ul/li/div/a/@href")
        except:
            pass
        else:
            return list_url_solve

    def parse(self,url_list):

        dict1 = {}
        for i in url_list:
            try:
                seponse=requests.get(i,headers=self.headers)
                html=etree.HTML(seponse.content)
                dict1['url']=i

                dict1['question'] = html.xpath("//div[@class='wdms']/div[3]/p[1]/text()")[0]
                if len(dict1['question'])==0:
                    continue
                dict1['describe'] = html.xpath("//div[@class='wdms']/div[3]/p[2]/text()")[0]
                if len( dict1['describe'])==0:
                    continue
                m=html.xpath("//div[@class='best_answer_show']/text()")
                d=''.join(m)
                r=d.replace('\r','').replace('\n','').replace('\u3000\u3000','')
                dict1['answer']=r
                if    dict1['answer']==0:
                    continue
                val=dict1.values()


                json1 = json.dumps(dict1, ensure_ascii=False)
                print(json1)

                fileOb = open('dcpfb.json', 'a+', encoding='utf-8', )  # 打开一个文件，没有就新建一个

                fileOb.write(json1 + ',' + '\n')

                fileOb.close()

            except:
              pass

    def run(self):
        n = 4638
        while n < 4884:
            self.url = 'http://www.dcpfb.com/ask/browser-lm-3-{}.html'.format(n)
            next_url=self.url
            n+=1
            print(self.url)
            time.sleep(3)
            url_list = self.data_url(next_url)
           # if len(url_list) == 0:
                #continue

            self.parse(url_list)

            next_url = 'http://www.dcpfb.com/ask/browser-lm-3-{}.html/'.format(n)

        print('结束')

dcpfb=Dcpfb()
dcpfb.run()


