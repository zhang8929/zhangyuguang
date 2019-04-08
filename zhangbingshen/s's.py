import requests
from lxml import etree
import json
import time

from selenium import webdriver

class Yishengshuo():
    '''医生说'''
    def __init__(self):
        self.url='http://doc.39.net/myzx/1.html'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}

    def frist_url(self):
        try:
            rep=requests.get(self.url,headers=self.headers)
            html=etree.HTML(rep.text)
            f_url=html.xpath('//*[@class="yss_left_nav l"]/ul/li/a/@href')[1::]
        except:
            pass

        else:
         return f_url
    def sed_url(self,i):
        s_url="http://doc.39.net"+i


        try:
            s_sep=requests.get(s_url,headers=self.headers)
            s_html=etree.HTML(s_sep.text)
            s_urls=s_html.xpath('//ul[@id="ulActivitys"]/li/div[2]/h2/a/@href')

        except:
            pass
        else:
            return s_urls

    def parse(self,p_url):
          #'下一页'：'http://doc.39.net/myzx/activity/_Index/584.html?pageIndex=2&pageSize=10'
        next_url="http://doc.39.net"+p_url
        next = 0
        while next<10:
            try:

                    p_sep=requests.get(next_url,headers=self.headers)
                    print('zhangbiingsn',next_url)
                    k=p_url.split('/')

                    p_html=etree.HTML(p_sep.text)
                    next += 1
                    print(next)
                    next_url = 'http://doc.39.net/' + k[1] + '/' + k[2] + '/' + '_Index' + '/' + k[3] + '?pageIndex={}&pageSize=10'.format(next)
                    for i in range(1, 11):

                        item = {}
                        item['url']=next_url
                        item['question'] =p_html.xpath('//li[{}]/div[@class="ask_text bgb pad20"]/div[2]/h2/text()'.format(i))[0]
                        if  len(item['question'])==0:
                            print(333)
                            break

                        item['describe'] = p_html.xpath('//li[{}]/div[@class="ask_text bgb pad20"]/div[2]/p/text()'.format(i))[0].replace('\r\n','').replace(' ','')
                        item['answer'] = p_html.xpath('//li[{}]/div[2]/div[2]/p/text()'.format(i))[0].replace('\r\n','').replace(' ','')


                        if len(item['question']) == 0:
                           print('tiaochu')
                           break
                        print(item)

                        item_json=json.dumps(item,ensure_ascii=False)
                        with open('yss.json','a',encoding='utf-8') as f:
                            f.write(item_json+','+'\n')


            except:
                pass







    def run(self):
        f_url=self.frist_url()
        for i in f_url:
            print("科室也",i)
            s_url=self.sed_url(i)

            for p_url in s_url:
                print("医生页面",p_url)


                self.parse(p_url)




yss=Yishengshuo()
yss.run()