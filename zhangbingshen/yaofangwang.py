import requests
from lxml import etree
import json
import time

class YaoFangWang():

    def __init__(self):
        self.url='https://www.yaofangwang.com/ask/quanbu/s2/'
        self.headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}

    def fist_url(self,next_rul):
        try:
            sep = requests.get(next_rul,headers=self.headers)
            html = etree.HTML(sep.content)
            url_list = html.xpath("//ul[@class='ques-list all-cat']/li/div/a/@href")
        except:
            pass
        else:
         return url_list

    def parse(self,url_list):
        dict1 = {}
        for i in url_list:
            try:
                urls='https:'+i
                reps=requests.get(urls,headers=self.headers)
                html_par=etree.HTML(reps.content)
                dict1['url']=urls
                dict1['question']=html_par.xpath('//*[@id="aspnetForm"]/div[4]/div[1]/div/div[1]/span/text()')[0]
                dict1['describe'] =html_par.xpath('//*[@id="aspnetForm"]/div[4]/div[1]/div/p/text()')[0].replace('\r','').replace('\n','').strip()
                dict1['answer']=html_par.xpath("//div[@class='ask-item']/div[2]/p/text()")[0].replace('\r','').replace('\n','').strip()
                json1 = json.dumps(dict1, ensure_ascii=False)
                print(json1)
                with open('yaofangwang.json', 'a+', encoding='utf-8', ) as f:  # 打开一个文件，没有就新建一个

                    f.write(json1 + ',' + '\n')
            except:
                pass



    def run(self):
        n=1
        while n<1016:
            print(n)
            next_url='https://www.yaofangwang.com/ask/quanbu/s2/p{}/'.format(n)

            url_list=self.fist_url(next_url)
            print(url_list)
            self.parse(url_list)
            n+=1
        print('结束')







yangfangwang=YaoFangWang()
yangfangwang.run()




