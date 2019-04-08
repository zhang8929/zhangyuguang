import requests
import requests
from lxml import etree
import  json
import random
import time

class Ask():
    def __init__(self):
        self.url='http://ask.ca39.com/'
        self.headers = [
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',

'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',

'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',

'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',

'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',

'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',

'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',

'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',

'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12']
    def frist_url(self):
       time.sleep(1)
       rep= requests.get(self.url)

       html= etree.HTML(rep.text)
       urls=html.xpath('//div[@class="category-nav"]/a/@href')

       return urls
    def parse(self,next_url):
        n_url = next_url.split("/")
        print(next_url)

        lis1=[]
        n=1
        while n<501:

            try:
                #agent = random.choice(self.headers)
                time.sleep(2)
                p_sep=requests.get(next_url,headers=random.randint(0,9))
                print(p_sep)
                html=etree.HTML(p_sep.text)
                sen_url=html.xpath('//div[@class="bd"]/div[1]//div/div/a/@href')
                if len(sen_url)==0:
                    print('tiaochu')
                    break
                lis1.append(sen_url)
                n += 1
                next_url=n_url[0]+'//'+n_url[2]+'/'+n_url[3]+'/'+n_url[4]+'/'+'all'+'/'+"{}.html".format(n)

                print(next_url)
                #'http://ask.ca39.com/c/55/all/2.html'
            except:
                pass
        print(lis1)
        return lis1

    def cont(self,q):
        for i in q:
            try:
                time.sleep(2)
                consep=requests.get(i,headers=self.headers[random.randint(0,9)])
                html=etree.HTML(consep.text)
                dict1={}
                dict1['question']=html.xpath('//div[@class="title pd40"]/h1/text()')[0]
                dict1['discilbe']=html.xpath('//div[@class="description"]/text()')[0].replace('\r\n','').replace(' ','')
                dict1['answer']=html.xpath('//*[@class="net-answer-list"]/li[1]/div/div[4]/text()')[1].replace('\r\n','').replace(' ','')

                josn_item = json.dumps(dict1, ensure_ascii=False)
                print(josn_item)
                with open('ask_ca39.json', 'a', encoding='utf-8')as f:
                    f.write(josn_item + ',' + '\n')
            except:
                pass


    def run(self):

          i='http://ask.ca39.com/c/32/all.html'
          ls_urls=self.parse(i)
          for q in ls_urls:
           self.cont(q)

sak=Ask()
sak.run()