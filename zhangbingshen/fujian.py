import requests
import json
from lxml import etree


class Ask():
    def __init__(self):
        self.url='http://ask.ca39.com/c/34.html'
        self.headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                     }

    def frist_url(self):
       resp= requests.get(self.url,headers=self.headers)
       print(resp)
       html = etree.HTML(resp.text)
       sen_url = html.xpath('//div[@class="bd"]/div[1]//div/div/a/@href')
       print(sen_url)
       for i in sen_url:
           co_sep=requests.get(i,headers=self.headers)
           print(co_sep)
          html= etree.HTML(co_sep.text)










a=Ask()

print(a.frist_url())
