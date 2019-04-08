import requests
import re
import json
from lxml import etree
class FamilyDocter():
    def __init__(self):
        self.url='http://why.familydoctor.com.cn/category/?page=1&'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}

    def first_url(self):
        '''科室列表'''
        try:
            n=0
            list1=[]
            while n<94:
                n+=1
                url='http://why.familydoctor.com.cn/category/?page={}&'.format(n)
                print(url)

                sep=requests.get(url,headers=self.headers)
                if sep.status_code==500:
                    continue

                html=etree.HTML(sep.text)

                urls=html.xpath('//*[@class="moduleContent"]/div/div[1]/a/@href')


                list1.append(urls)

            return list1
        except:
            pass
    def sent_url(self,i):

        try:
            n=0
            while n <121:
                n+=1
                k = i + '?page={}&'.format(n)
                print(k)
                sent_sep=requests.get(k,headers=self.headers)
                if sent_sep.status_code==500:
                    continue
                sent_html= etree.HTML(sent_sep.text)
                cont_urls=sent_html.xpath("//div[@class='moduleContent']/div/div/h3/a/@href")
                if len(cont_urls)==0:
                    break

                for j in cont_urls:

                    dict1={}
                    cen_sep= requests.get(j,headers=self.headers)
                    if sent_sep.status_code==500:
                        continue
                    cen_html=etree.HTML(cen_sep.text)
                    m=cen_html.xpath("//div[@class='ksItem']//h3/text()")
                    if len(m)>0:
                         dict1['question']=''.join(m).replace('\r\n','').replace(' ','')
                    q=cen_html.xpath("//div[@class='itemText']/p//text()")
                    if len(q)>0:
                         dict1['answer']=''.join(q).replace('\r\n','').replace(' ','').replace('\n','').replace('\u3000','')


                    json_dict1=json.dumps(dict1,ensure_ascii=False)
                    print(json_dict1)
                    with open('famliy_doctor.json','a',encoding='utf-8')as f:
                        f.write(json_dict1+','+'\n')
        except:
            pass




    def run(self):
        list1=self.first_url()
        for urls in list1:

            for i in urls:
                 self.sent_url(i)



fam=FamilyDocter()
fam.run()