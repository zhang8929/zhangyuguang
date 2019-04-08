import  requests
import json
from lxml import etree

class Wyjy():
    def __init__(self):
        self.url='http://www.51jiuyi.cn/ask/list_21_0_1_1.html'

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
    def frist_url(self):
        try:
            next_list=self.url.split('/')

            str_ur=next_list[len(next_list)-1].split('_')

            htm=str_ur[len(next_list)-1].replace('1','{}')

            n =0
            while n < 30000:

                n+=1
                print(n)
                next_url = next_list[0] + '/' + next_list[1] + '/' + next_list[2] + '/' + next_list[3] + '/' + str_ur[
                    0] + '_' + str_ur[1] + '_' + str_ur[2] + '_' + str_ur[3] + '_' + htm.format(n)
                print(next_url)
                sep=requests.get(next_url,headers=self.headers)
                print(sep)

                html=etree.HTML(sep.text)
                url_li=html.xpath("//*[@class='show_hide']/li[1]/ul/li/a[2]//@href")
                if len(url_li)==0:
                    break
                print(len(url_li))
                print(url_li)

                for i in  url_li:
                    dict1={}
                    urs='http://www.51jiuyi.cn'+i

                    con_sep=requests.get(urs,headers=self.headers)
                    con_html=etree.HTML(con_sep.text)
                    question=con_html.xpath("//*[@class='huanzhetiwen']/h3//text()")
                    dict1['question']=''.join(question).replace('\n','').replace('                            ','').replace('\n','').replace('\t','').replace('\r','')
                    answer=con_html.xpath("//*[@class='yisheng_jieda']/div[1]/div[2]/ul/li[1]//text()")
                    dict1['answer']=''.join(answer).replace('\xa0 \xa0 \xa0 病情分析：\r\n\xa0\xa0\xa0\xa0\xa0\xa0','').replace('\u3000\u3000','').replace('\r\n\xa0\xa0\xa0\xa0\xa0\xa0指导意见：\r\n\xa0\xa0\xa0\xa0\xa0\xa0','').replace('\n','').replace('\t','').replace('\r','')


                    json_dict=json.dumps(dict1,ensure_ascii=False)
                    print(json_dict)
                    with open('erbihou.json','a',encoding='utf-8')as f :
                        f.write(json_dict+','+'\n')
        except:
            pass





    def run(self):
        self.frist_url()




wyjy=Wyjy()
wyjy.run()