import requests
import json
from lxml import etree
class Xunyi():
    def __init__(self):
        self.url='http://zzk.fh21.com.cn/letter/symptoms/S-4.html'
        self.headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1' }
    def first_url(self,url):
        sep = requests.get(url, headers=self.headers)
        if sep.status_code == 404:
           pass
        html = etree.HTML(sep.text)
        list_url = html.xpath('//*[@id="illA"]/ul/li/a/@href')
        return list_url

    def sencon(self,li):
        dict1={}
        urls='http://jib.xywy.com'+li
        sen_sep= requests.get(urls,headers=self.headers)
        sen_html=etree.HTML(sen_sep.text)
        zhen_url=sen_html.xpath("//*[@class='jib-navbar fl bor pr']/div[2]/ul/li[1]/a/@href")[0]
        zhen_sep=requests.get(zhen_url,headers=self.headers)
        zhen_html=etree.HTML(zhen_sep.text)
        tile=zhen_html.xpath("//*[@class='wrap mt5']/div/text()")
        dict1['title']=''.join(tile)
        symptom=zhen_html.xpath("//*[@class='jib-articl fr f14 jib-lh-articl']/p//text()")
        dict1['symptom']=''.join(symptom)
        changjian=zhen_html.xpath("//*[@class='jib-articl fr f14 jib-lh-articl']/span/a/@href)")

        json_dict1=json.dumps(dict1,ensure_ascii=False)
        with open('xun.json','a',encoding='utf-8')as f:
            f.write(json_dict1+','+'\n')

        for cha in changjian:
            cha_sep=requests.get(cha,headers=self.headers)
            cha_html=etree.HTML(cha_sep.text)
            xiangqing=cha_html.xpath("//*[@class='jib-rec-hd clearfix']/p/a/@href")[0]
            xiang_url='http://jib.xywy.com'+xiangqing
            xiang_sep=requests.get(xiang_url,headers=self.headers)
            xiang_html=etree.HTML(xiang_sep.text)

            tile = xiang_html.xpath("//*[@class='wrap mt5']/div/text()")
            dict1['title'] = ''.join(tile)
            symptom = xiang_html.xpath("//*[@class='zz-articl fr f14']/div[1]//text()")
            dict1['symptom'] = ''.join(symptom)

            json_dict1 = json.dumps(dict1, ensure_ascii=False)
            with open('xun.json', 'a', encoding='utf-8')as f:
                f.write(json_dict1 + ',' + '\n')

    def run(self):
        zimu=['a', 'b', 'c', 'd' ,'e', 'f', 'g' ,'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
        for i in zimu:
             url='http://jib.xywy.com/html/{}.html'.format(i)
             lisst1=self.first_url(url)
             for li in lisst1:
                 self.sencon(li)
