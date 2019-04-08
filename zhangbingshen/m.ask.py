import requests
import json
from lxml import etree

class Mask():
    def __init__(self):
        self.url='http://m.ask.j1.com/keshi/'
        self.headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                     }
    def frist_url(self):
        sep=requests.get(self.url,headers=self.headers)
        print(sep)
        html=etree.HTML(sep.content)
        f_url=html.xpath('//section[@class="siteNav"]/ul/li/ul/li/a/@href')
        return f_url
    def cen_url(self,cond_url):
        cen_urls=requests.get(cond_url,headers=self.headers)
        html=etree.HTML(cen_urls.content)
        centen_urls=html.xpath('//ul[@class="clearfix data-list"]/a/@href')
        print(centen_urls)
        return centen_urls
    def content_url(self,content):
        centent_url=requests.get(content)
        html=etree.HTML(centent_url.text)
        item={}
        item['url']=content
        item['question']=html.xpath('//div[@class="ask_info"]/p/a/text()')[0]
        item['describe'] = html.xpath('//div[@class="det"]/p/text()')[0].replace('\n','').replace(' ','')
        m= html.xpath('//div[@class="docInfo clearfix"]/dl/dd/p[2]/text()')
        if len(m)==0:
            pass


        item['answer']=m
        json_item=json.dumps(item,ensure_ascii=False)
        print(json_item)
        with open('m-sak.json','a',encoding='utf-8')as f:
            f.write(json_item+','+'\n')

    def run(self):
        f_url=self.frist_url()
        print(len(f_url))
        print(f_url)
        for i in f_url:
            print(i)
            cond_url="http://m.ask.j1.com"+i
            print(cond_url)
            centen_urls=self.cen_url(cond_url)
            for q in centen_urls:
                content="http://m.ask.j1.com"+q
                self.content_url(content)


mask=Mask()
mask.run()