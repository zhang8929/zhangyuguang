import requests
import re
from lxml import etree
import json
class Feihua():
    def __init__(self):
        self.url='http://zzk.fh21.com.cn/letter/symptoms/S-4.html'
        self.headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1' }
    def first(self,url):
        try:
            lisst1=[]
            n=0
            u_list=url.split('/')
            html_url =u_list[len(u_list)-1].split('.')
            while n<10:
                n+=1
                url = u_list[0] + u_list[1]+'//' + u_list[2] + '/' + u_list[3] + '/' + u_list[4] + '/' + html_url[
                    0] + '-' +str(n)+ '.' + html_url[1]
                print(url)
                sep=requests.get(url,headers=self.headers)
                if sep.status_code==404:
                    continue
                html=etree.HTML(sep.text)
                list_url=html.xpath("//*[@class='border03_body']/ul/li/a/@href")
                if len(list_url)>0:
                    lisst1.append(list_url)
                continue
            print(lisst1)
        except:
            pass
        else:
             return lisst1

    def sencon(self,li):


        for l in li:
         try:
            dict1={}
            urls='http://zzk.fh21.com.cn'+l
            sen_sep=requests.get(urls,headers=self.headers)
            sen_html=etree.HTML(sen_sep.text)
            quanwen=sen_html.xpath("//*[@class='main_content']/ul[1]/dl/dd/a/@href")
            urles = 'http://zzk.fh21.com.cn' + quanwen[0]
            sens_sep=requests.get(urles,headers=self.headers)
            sens_html=etree.HTML(sens_sep.text)
            title=sens_html.xpath("//*[@class='submenu']/ul[1]/div/h2/strong/a//text()")
            dict1['title']=''.join(title)
            intro=sens_html.xpath("//*[@class='main_content']/ul[1]/div[1]/div[1]//text()")
            dict1['intro']=''.join(intro)

            print(dict1)
            json_dict1=json.dumps(dict1,ensure_ascii=False)
            with open('feihua.json','a',encoding='UTF-8')as f:
                f.write(json_dict1+','+'\n')
         except:
             continue




    def run(self):
        zimu=[ 'N', 'O','P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ]
        for i in zimu:
             url='http://zzk.fh21.com.cn/letter/symptoms/{}.html'.format(i)
             lisst1=self.first(url)
             for li in lisst1:
                 self.sencon(li)


feihua=Feihua()
feihua.run()