import re
import requests
import json
from lxml import etree

class BaoZhiLin():
     def __init__(self):
         self.url=''
         self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
     def fisrt_url(self,url):
         n=0
         list1=[]
         while n<721:
             fen=url.split('_')
             fen[3]='{}.html'.format(n)
             url=str(fen[0])+'_'+fen[1]+'_'+fen[2]+'_'+fen[3]
             n += 90
             sep=requests.get(url,headers=self.headers)
             html=etree.HTML(sep.text)
             li=html.xpath("//ul[@class='textList clearfix']/li/a/@href")
             print(li,'列表')
             if len(li)>0:
                  list1.append(li)
             if len(li)==0:
                 break

         print(list1)
         return list1
     def sontend(self,son):
         for  so in son:
            try:
             dict1={}
             son_url='http://www.360bzl.com'+so
             son_sep=requests.get(son_url,headers=self.headers)
             son_html=etree.HTML(son_sep.text)
             title=son_html.xpath("//div[@class='main_title']/span//text()")
             dict1['title']=''.join(title)

             fen_so= so.split('/')
             print(fen_so)
             so_url='/'+fen_so[0]+fen_so[1]+'/'+fen_so[2]+'/'
             so_url = 'http://www.360bzl.com' + so_url
             gai_sep = requests.get(so_url, headers=self.headers)

             gai_html = etree.HTML(gai_sep.text)
             dict2={}
             list2=[]
             for u in range(1,8):
                 name=gai_html.xpath("//div[@class='direction']/p[{}]/text()".format(u))
                 if len(name)>0:
                     name=''.join(name)
                     cont=gai_html.xpath("//div[@class='direction']/p[{}]/span//text()".format(u))
                     cont=' '.join(cont)
                     if len(cont)==0:
                         cont = gai_html.xpath("//div[@class='direction']/p[{}]/a//text()".format(u))
                         cont = ' '.join(cont)
                     dict2[name]=cont

             # list2.append(dict2)
             # print(list2)
             dict1['summarize']=dict2



             name_sms = son_html.xpath("//div[@class='main_left']/div/span//text()")
             name_sms = ''.join(name_sms)
             list3=[]
             dict3={}
             dict3_1={}
             dict3['name_sms'] = name_sms
             for sms in range(1,15):
                 title_sms=son_html.xpath("//div[@class='main_left']/p[{}]/text()".format(sms))
                 if len(title_sms)>0:
                     title_sms=''.join(title_sms)
                     cont_sms=son_html.xpath("//div[@class='main_left']/p[{}]/span//text()".format(sms))
                     if len(cont_sms)==0:
                         cont_sms = son_html.xpath("//div[@class='main_left']/p[{}]/a//text()".format(sms))
                     cont_sms = ' '.join(cont_sms)
                     dict3[title_sms]=cont_sms
             dict3_1[name_sms]=dict3
             dict1['specification']=dict3_1


             gxzy_url=so.split('/')

             gxzy_url = '/' + gxzy_url[0] + gxzy_url[1] + '/' + gxzy_url[2] + '/'+'gxzy'+'/'

             gxzy_url = 'http://www.360bzl.com' + gxzy_url

             gxzy_sep=requests.get(gxzy_url,headers=self.headers)
             gxzy_html=etree.HTML(gxzy_sep.text)
             dict4={}
             name_gxzy=gxzy_html.xpath("//div[@class='main_left']/div[1]/span/text()")
             name_gxzy=''.join(name_gxzy)
             cont_gxzy=gxzy_html.xpath("//div[@class='main_left']/p//text()")
             cont_gxzy=''.join(cont_gxzy)
             dict4[name_gxzy]=cont_gxzy

             dict1['efficacy']=dict4

             yfyl_url = so.split('/')

             yfyl_url = '/' + yfyl_url[0] + yfyl_url[1] + '/' + yfyl_url[2] + '/' + 'yfyl' + '/'

             yfyl_url = 'http://www.360bzl.com' + yfyl_url

             yfyl_sep = requests.get(yfyl_url, headers=self.headers)
             yfyl_html = etree.HTML(yfyl_sep.text)
             dict5 = {}
             name_yfyl = yfyl_html.xpath("//div[@class='main_left']/div[1]/span/text()")
             name_yfyl = ''.join(name_yfyl)
             cont_yfyl = yfyl_html.xpath("//div[@class='main_left']/p//text()")
             cont_yfyl= ''.join(cont_yfyl)
             dict5[name_yfyl] = cont_yfyl

             dict1['instruction'] = dict5

             blfy_url = so.split('/')

             blfy_url = '/' + blfy_url[0] + blfy_url[1] + '/' + blfy_url[2] + '/' + 'fzy' + '/'

             blfy_url = 'http://www.360bzl.com' + blfy_url

             blfy_sep = requests.get(blfy_url, headers=self.headers)
             blfy_html = etree.HTML(blfy_sep.text)
             dict6 = {}
             name_blfy = blfy_html.xpath("//div[@class='main_left']/div[1]/span/text()")
             name_blfy = ''.join(name_blfy)
             cont_blfy = blfy_html.xpath("//div[@class='main_left']/p//text()")
             cont_blfy = ''.join(cont_blfy)
             dict6[name_blfy] = cont_blfy

             dict1['adverse_reaction'] = dict6

             jj_url = so.split('/')

             jj_url = '/' + jj_url[0] + jj_url[1] + '/' + jj_url[2] + '/' + 'jj' + '/'

             jj_url = 'http://www.360bzl.com' + jj_url

             jj_sep = requests.get(jj_url, headers=self.headers)
             jj_html = etree.HTML(jj_sep.text)
             dict7 = {}
             name_jj = jj_html.xpath("//div[@class='main_left']/div[1]/span/text()")
             name_jj = ''.join(name_jj)
             cont_jj = jj_html.xpath("//div[@class='main_left']/p//text()")
             cont_jj = ''.join(cont_jj)
             dict7[name_jj] = cont_jj

             dict1['taboo'] = dict7

             zysx_url = so.split('/')

             zysx_url = '/' + zysx_url[0] + zysx_url[1] + '/' + zysx_url[2] + '/' + 'zysx' + '/'

             zysx_url = 'http://www.360bzl.com' + zysx_url

             zysx_sep = requests.get(zysx_url, headers=self.headers)
             zysx_html = etree.HTML(zysx_sep.text)
             dict8 = {}
             name_zysx = zysx_html.xpath("//div[@class='main_left']/div[1]/span/text()")
             name_zysx = ''.join(name_zysx)
             cont_zysx = zysx_html.xpath("//div[@class='main_left']/p//text()")
             cont_zysx = ''.join(cont_zysx)
             dict8[name_zysx] = cont_zysx
             print(dict8, 'bing')
             dict1['taboo'] = dict8

             js_dict=json.dumps(dict1,ensure_ascii=False)
             print(js_dict)
             with open('baozhilin.json','a',encoding='utf-8')as f:
                 f.write(js_dict+','+'\n')
            except:
                pass

     def run(self):
         lie=['b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
         for i in lie:
              print(i)
              url='http://www.360bzl.com/ypk/pylist_3_{}_0.html'.format(i)
              list1=self.fisrt_url(url)
              print(len(list1))

              for son in list1:
                 self.sontend(son)
bao=BaoZhiLin()
bao.run()
