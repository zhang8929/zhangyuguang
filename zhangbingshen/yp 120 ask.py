import requests
import re
import json
from lxml import etree

class YP():
    def __init__(self):
        self.url='https://yp.120ask.com/exp/list/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
    def frist_url(self):
        try:
            n=0

            while n<9813:
                n+=1
                url=self.url+'?page={}'.format(n)
                print(url)
                sep=requests.get(url,headers=self.headers)
                if sep.status_code==500:
                    continue
                html=etree.HTML(sep.text)
                url_list= html.xpath("//div[@class='drugListPart']/dl/dd/b/a/@href")
                print(url_list)
                for i in url_list:

                    sep_con=requests.get(('https:'+i),headers=self.headers)
                    if sep_con.status_code==500:
                        continue
                    html_con=etree.HTML(sep_con.content)
                    dict1={}
                    m=html_con.xpath("//div[@class='ti']/h1/text()")
                    if len(m)>0:
                        dict1['title']=''.join(m)
                    q=html_con.xpath('//div[@class="exp_box1"]/p[2]/span/text()')
                    if len(q)>0:
                        dict1['disclibe']=''.join(q)

                    w = html_con.xpath('//div[@class="exp_box1"]/p[3]/span/text()')
                    if len(q) > 0:
                        dict1['illness_name '] = ''.join(w)
                    e = html_con.xpath('//div[@class="exp_box1"]/p[4]/span/text()')
                    if len(q) > 0:
                        dict1['symptom'] = ''.join(e)
                    t = html_con.xpath('//div[@class="Reviews_about Reviews_about1 clears"]/div/p/text()')
                    if len(q) > 0:
                        dict1['answer'] = ''.join(t)

                    json_dict=json.dumps(dict1,ensure_ascii=False)
                    print(json_dict)
                    with open('yo_120ask.json','a',encoding='utf-8')as f :
                        f.write(json_dict+','+'\n')
        except:
            pass




    def run(self):
        url_list=self.frist_url()


yp=YP()
yp.run()