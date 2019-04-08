import requests
import json
import re
from lxml import etree

class Tag_120():
    def __init__(self):
        self.url='https://tag.120ask.com/jibing/pinyin/f.html'

        self.headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
                      }
    def first_url(self,url):
        try:
            f_sep=requests.get(url,headers=self.headers)
            if f_sep.status_code==404:
                return '有问题'
            if f_sep.status_code==500:
                return '服务器错误'
            html_f=etree.HTML(f_sep.text)
            url_list=html_f.xpath('//div[@class="tag_li"]/p[1]/a/@href')

        except:
            pass
        else:
             return url_list
    def shiliao(self,j):

        try:
            urls='https://tag.120ask.com/jibing'+j

            sen_sep=requests.get(urls,headers=self.headers)

            if sen_sep.status_code==500:
                return '服务器错误'

            sen_html= etree.HTML(sen_sep.text)

            sen_urls=sen_html.xpath("//*[@class='disease-list-right']//a/@href")
            print(sen_urls)
            url_shi=j+'shiliao/'
            url_bing = j + 'bingyin/'
            url_zheng= j + 'zhengzhuang/'
            url_cha = j + 'jiancha/'
            url_jia= j + 'jianbie/'
            url_fa = j + 'bingfa/'
            url_yu = j + 'yufang/'
            url_zhi = j + 'zhiliao/'
            url_yi = j + 'yinshi/'

            return url_shi,url_bing,url_fa,url_zheng,url_cha,url_jia,url_yu,url_zhi,url_yi
        except:
            pass
    def pare(self,url_shi, url_bing, url_fa, url_zheng, url_cha,url_jia, url_yu, url_zhi, url_yi):
        try:
            dict1={}
            con_url='https://tag.120ask.com'+url_shi
            con_sep=requests.get(con_url,headers=self.headers)
            if con_sep.status_code==404:
                print('404')
                pass

            con_html=etree.HTML(con_sep.text)
            title = con_html.xpath("//*[@class='top_dl']/b//text()")
            if len(title)>0:
                dict1['title']=title[0]
            str_yi=con_html.xpath("//*[@class='wrap_big']/div[1]/span/var/text()")
            if len(str_yi)>0:

                str_yi=''.join(str_yi).replace('\r','').replace('\n','').replace('   ','')
            list2=[]
            for k in range(1,6):
                classify_fist=con_html.xpath("//*[@class='dl_1']/div/div[1]/div[1]/div[{}]/em//text()".format(k))
                if len(classify_fist)>0:
                    classify_fist=''.join(classify_fist).replace('\t','').replace('\n',' ').replace('\r','').replace('        ','')
                    if classify_fist != '  ':
                        classify_fist_con=con_html.xpath("//*[@class='dl_1']/div/div[5]/div[{}]//text()".format(k))
                        classify_fist_con= ''.join(classify_fist_con).replace('\t','').replace('\n',' ').replace('\r','')


                        classify_con=classify_fist+'：'+classify_fist_con
                        list2.append(classify_con)

                else:
                    continue


            classify=str_yi+''.join(list2)

            dict1['suitable']=classify




    # =================================忌=================================================================================/=


            str_ji=con_html.xpath("//*[@class='wrap_big']/div[2]/span/var/text()")
            str_ji=''.join(str_ji).replace('\r','').replace('\n','').replace('   ','')
            list3=[]
            for z in range(1,6):
                ji_fist=con_html.xpath("//*[@class='dl_2']/div/div[1]/div[1]/div[{}]/em//text()".format(z))

                if len(ji_fist)>0:

                    ji_fist=''.join(ji_fist).replace('\t','').replace('\n',' ').replace('\r','').replace('        ','')

                    if ji_fist!='  ':

                        ji_fist_con=con_html.xpath("//*[@class='dl_2']/div/div[5]/div[{}]//text()".format(z))
                        ji_fist_con= ''.join(ji_fist_con).replace('\t','').replace('\n',' ').replace('\r','')

                        ji_con=ji_fist+'：'+ji_fist_con
                        list3.append(ji_con)



                else:
                    continue

            ji=str_ji+''.join(list3)

            dict1['taboo']=ji
            # ===================================================================================================================/=
            bing_url = 'https://tag.120ask.com' + url_bing
            bing_sep = requests.get(bing_url, headers=self.headers)
            bing_html = etree.HTML(bing_sep.text)
            bing = bing_html.xpath("//*[@class='art_cont']//text()")
            bing=''.join(bing).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['pathogeny']=bing

            zheng_url = 'https://tag.120ask.com' + url_zheng
            zheng_sep = requests.get(zheng_url, headers=self.headers)
            zheng_html = etree.HTML(zheng_sep.text)
            zheng = zheng_html.xpath("//*[@class='art_cont']//text()")
            zheng = ''.join(zheng).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['symptom'] = zheng

            cha_url = 'https://tag.120ask.com' + url_cha
            cha_sep = requests.get(cha_url, headers=self.headers)
            cha_html = etree.HTML(cha_sep.text)
            cha = cha_html.xpath("//*[@class='art_cont']//text()")
            cha = ''.join(cha).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['examine'] = cha

            jia_url = 'https://tag.120ask.com' + url_jia
            jia_sep = requests.get(jia_url, headers=self.headers)
            jia_html = etree.HTML(jia_sep.text)
            jia = jia_html.xpath("//*[@class='art_cont']//text()")
            jia= ''.join(jia).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['identify'] = jia

            fa_url = 'https://tag.120ask.com' + url_fa
            fa_sep = requests.get(fa_url, headers=self.headers)
            fa_html = etree.HTML(fa_sep.text)
            fa = fa_html.xpath("//*[@class='art_cont']//text()")
            fa = ''.join(fa).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['complication'] = fa

            yu_url = 'https://tag.120ask.com' + url_yu
            yu_sep = requests.get(yu_url, headers=self.headers)
            yu_html = etree.HTML(yu_sep.text)
            yu = yu_html.xpath("//*[@class='art_cont']//text()")
            yu = ''.join(yu).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['prevent'] = yu

            zhi_url = 'https://tag.120ask.com' + url_zhi
            zhi_sep = requests.get(zhi_url, headers=self.headers)
            zhi_html = etree.HTML(zhi_sep.text)
            zhi = zhi_html.xpath("//*[@class='art_cont']//text()")
            zhi = ''.join(zhi).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['cure '] = zhi

            yi_url = 'https://tag.120ask.com' + url_yi
            yi_sep = requests.get(yi_url, headers=self.headers)
            yi_html = etree.HTML(yi_sep.text)
            yi = yi_html.xpath("//*[@class='art_cont']//text()")
            yi = ''.join(yi).replace('\t','').replace('\r','').replace('\n','').replace('                 　　',' ').replace('　　',' ').replace('                 ',' ')
            dict1['diet '] = yi


            json_dict=json.dumps(dict1,ensure_ascii=False)
            print(json_dict)
            with open('tag.json','a',encoding='utf-8')as f:

                f.write(json_dict+','+'\n')
        except:
            pass





    def run(self):
        list1=['y']
        for i in list1:
          try:
            print(i,'字母')
            url='https://tag.120ask.com/jibing/pinyin/{}.html'.format(i)
            url_list=self.first_url(url)
            print(url_list)
            print(len(url_list),'个数')

            for j in url_list:
                try:
                    print(j,url_list.index(j))
                    url_shi, url_bing, url_fa, url_zheng, url_cha,url_jia, url_yu, url_zhi, url_yi=self.shiliao(j)

                    self.pare(url_shi, url_bing, url_fa, url_zheng, url_cha,url_jia, url_yu, url_zhi, url_yi)
                    print(url_shi)
                except:
                    continue
          except:
              continue



tag=Tag_120()
tag.run()