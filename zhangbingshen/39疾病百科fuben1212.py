import requests
import re
import json
from lxml import etree

class JbBk():
    '''疾病百科'''
    def __init__(self):
        self.url='http://jbk.39.net/map/jb/jbgs/'
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",}
    def first_url(self):


                # urls='http://jbk.39.net/map/jb/jbgs_p1'
                #
                # sep=requests.get(urls,headers=self.headers)
                #
                # html=etree.HTML(sep.content)
                # urls=html.xpath('//ul[@class="site-list"]/li/a/@href')
                #
                #
                # print(urls)
                # return urls

                n = 0
                list1 = []
                while n < 54:
                    n += 1
                    urls = 'http://jbk.39.net/map/jb/jbgs_p{}'.format(n)

                    sep = requests.get(urls, headers=self.headers)

                    html = etree.HTML(sep.content)
                    urls = html.xpath('//ul[@class="site-list"]/li/a/@href')
                    if len(urls) == 0:
                        break

                    list1.append(urls)

                return list1



    def send_url(self,urls):
      try:
        '''疾病概述解析'''
        n=1
        # list2=[]
        for i in urls:
            print('这是第内容列表层',i)
            print('这是序号',urls.index(i))
            n += 1
            print(len(urls), n)
            dict1 = {}
            print(i)
            sep=requests.get(i,headers=self.headers)
            if sep.status_code==500:
                print('chuchuo')
                continue
            html= etree.HTML(sep.content)

            z=html.xpath("//*[@class='disease_box']/div/h1/text()")
            if len(z)>0:
                 dict1['title']=''.join(z)

            b=html.xpath("//*[@class='information_box']/p/text()")
            if len(b)>0:
                dict1['disease']=''.join(b)


            url_list=html.xpath("//div[@class='left_navigation']/div/ul/li/a/@href")

            if len(url_list)==11 or len(url_list)==12 or len(url_list)==10:
                    print('==================shu')

# ----------------------------------------------------------------------------------------------------------------
                    sep_intro = requests.get(url_list[0], headers=self.headers)

                    if sep_intro.status_code==500:

                        continue

                    html_intro = etree.HTML(sep_intro.content)
                    x = html_intro.xpath("//div[@class='disease_box']/p[2]/text()")
                    if len(x) > 0:
                        dict1['illness_intro'] = ''.join(x)
                    list7=[]
                    for qw in range(1, 20):

                        dict2={}
                        abc_key= html_intro.xpath("//div[@class='list_left']/div[2]/ul/li[{}]/span[1]//text()".format(qw))
                        if len(abc_key)==0:
                            break
                        abc_keys= ''.join(abc_key).replace(' ','')
                        abc_value = html_intro.xpath("//div[@class='list_left']/div[2]/ul/li[{}]/span[2]//text()".format(qw))


                        abc_valuees = ''.join(abc_value).replace('\r\n','')
                        abc_values=abc_valuees.split(',')

                        dict2[abc_keys] = abc_valuees

                        diagnose_key =html_intro.xpath("//div[@class='list_left']/div[3]/ul/li[{}]/span[1]//text()".format(qw))
                        diagnose_keys=''.join(diagnose_key).replace(' ','')

                        diagnose_value = html_intro.xpath("//div[@class='list_left']/div[3]/ul/li[{}]/span[2]//text()".format(qw))
                        diagnose_valuees = ' '.join(diagnose_value).replace('\r\n','')
                        diagnose_values=diagnose_valuees.split(',')

                        dict2[diagnose_keys]= diagnose_valuees

                        hospital_see_key =html_intro.xpath("//div[@class='list_left']/div[4]/ul/li[{}]/span[1]//text()".format(qw))
                        hospital_see_keys=''.join(hospital_see_key).replace(' ','')
                        dict1['hospital_see_key']=hospital_see_keys
                        hospital_see_value = html_intro.xpath("//div[@class='list_left']/div[4]/ul/li[{}]/span[2]//text()".format(qw))
                        hospital_see_valuees = ' '.join(hospital_see_value).replace('\r\n','')

                        if len(hospital_see_key)>0:
                           dict2[hospital_see_keys]=hospital_see_valuees
                        list7.append(dict2)


                    dict1['disease_information']=list7


                    sep_symptom = requests.get(url_list[1], headers=self.headers)
                    if sep_symptom.status_code == 500:
                        print('505')
                        continue
                    html_sy = etree.HTML(sep_symptom.content)
                    t = html_sy.xpath("//div[@class='article_paragraph']/p//text()")
                    if len(t) > 0:
                        dict1['illness_symptom'] = ' '.join(t)

                    sep_pathogen = requests.get(url_list[2], headers=self.headers)
                    if sep_pathogen.status_code == 500:
                        print('urls+lsit[2]')
                        continue
                    html_pa = etree.HTML(sep_pathogen.content)
                    t_s = html_pa.xpath("//div[@class='article_paragraph']/p//text()")
                    if len(t_s) > 0:
                        dict1['illness_pathogen'] = ' '.join(t_s)


                    sep_complication = requests.get(url_list[3], headers=self.headers)
                    if sep_complication.status_code == 500:

                        continue

                    html_complication = etree.HTML(sep_complication.content)
                    t_c = html_complication.xpath("//div[@class='disease_box']/div[2]//p/text()")
                    if len(t_c) > 0:
                        dict1['illness_complication'] = ' '.join(t_c).replace('\r\n','')



                    sep_prevent = requests.get(url_list[4], headers=self.headers)
                    if sep_prevent.status_code == 500:

                        continue

                    html_pr = etree.HTML(sep_prevent.content)
                    t_p = html_pr.xpath("//div[@class='article_box']//p/text()")
                    if len(t_p) > 0:
                        dict1['illness_prevent'] = ' '.join(t_p)

                    sep_identify = requests.get(url_list[5], headers=self.headers)
                    if sep_identify.status_code == 500:

                        continue

                    html_identify = etree.HTML(sep_identify.content)
                    t_i = html_identify.xpath("//div[@class='article_box']//p/text()")
                    if len(t_i) > 0:
                        dict1['illness_identify'] = ' '.join(t_i)


                    sep_treat = requests.get(url_list[6], headers=self.headers)
                    if sep_treat.status_code == 500:

                        continue

                    html_treat = etree.HTML(sep_treat.content)
                    t_t = html_treat.xpath("//div[@class='article_box']//p/text()")
                    if len(t_t) > 0:
                        dict1['illness_treat'] = ' '.join(t_t)

                    sep_examine = requests.get(url_list[7], headers=self.headers)


                    if sep_examine.status_code == 500:

                        continue
                    html_examine = etree.HTML(sep_examine.content)
                    t_examine = html_examine.xpath("//div[@class='article_box']//p/text()")
                    if len(t_examine) > 0:
                        dict1['illness_examine'] = ' '.join(t_examine)

                    sep_nurse = requests.get(url_list[8], headers=self.headers)


                    if  sep_nurse.status_code == 500:

                        continue
                    html_nurse = etree.HTML(sep_nurse.content)
                    t_nurse = html_nurse.xpath("//div[@class='article_box']//p/text()")
                    if len(t_nurse) > 0:
                        dict1['illness_nurse'] = ' '.join(t_nurse)


                    diet= requests.get(url_list[9], headers=self.headers)


                    if diet.status_code == 500:

                        continue
                    html_diet = etree.HTML(diet.content)
                    t_diet = html_diet.xpath("//div[@class='article_box']//p/text()")
                    if len(t_diet) > 0:
                        dict1['diet'] = ' '.join(t_diet)

                    json_dict=json.dumps(dict1,ensure_ascii=False)

                    with open('39jibing3.json','a',encoding='utf-8')as f:
                        print(json_dict)
                        f.write(json_dict+','+'\n')
                    # list2.append(dict1)
  # =====================# ====================================================================================================

            else:
                print('**********dhda***********')

                # ----------------------------------------------------------------------------------------------------------------
                sep_intro = requests.get(url_list[0], headers=self.headers)

                if sep_intro.status_code == 500:
                    continue

                html_intro = etree.HTML(sep_intro.content)
                x = html_intro.xpath("//div[@class='disease_box']/p[2]/text()")
                if len(x) > 0:
                    dict1['illness_intro'] = ''.join(x)
                list7 = []
                for qw in range(1, 20):

                    dict2 = {}
                    abc_key = html_intro.xpath("//div[@class='list_left']/div[2]/ul/li[{}]/span[1]//text()".format(qw))
                    if len(abc_key) == 0:
                        break
                    abc_keys = ' '.join(abc_key).replace(' ', '')
                    abc_value = html_intro.xpath(
                        "//div[@class='list_left']/div[2]/ul/li[{}]/span[2]//text()".format(qw))

                    abc_valuees = ' '.join(abc_value).replace('\r\n', '')
                    abc_values = abc_valuees.split(',')

                    dict2[abc_keys] = abc_valuees

                    diagnose_key = html_intro.xpath(
                        "//div[@class='list_left']/div[3]/ul/li[{}]/span[1]//text()".format(qw))
                    diagnose_keys = ''.join(diagnose_key).replace(' ', '')

                    diagnose_value = html_intro.xpath(
                        "//div[@class='list_left']/div[3]/ul/li[{}]/span[2]//text()".format(qw))
                    diagnose_valuees = ' '.join(diagnose_value).replace('\r\n', '')
                    diagnose_values = diagnose_valuees.split(',')

                    dict2[diagnose_keys] = diagnose_valuees

                    hospital_see_key = html_intro.xpath(
                        "//div[@class='list_left']/div[4]/ul/li[{}]/span[1]//text()".format(qw))
                    hospital_see_keys = ''.join(hospital_see_key).replace(' ', '')
                    dict1['hospital_see_key'] = hospital_see_keys
                    hospital_see_value = html_intro.xpath(
                        "//div[@class='list_left']/div[4]/ul/li[{}]/span[2]//text()".format(qw))
                    hospital_see_valuees = ' '.join(hospital_see_value).replace('\r\n', '')

                    if len(hospital_see_key) > 0:
                        dict2[hospital_see_keys] = hospital_see_valuees
                    list7.append(dict2)

                dict1['disease_information'] = list7

                sep_symptom = requests.get(url_list[1], headers=self.headers)
                if sep_symptom.status_code == 500:
                    print('505')
                    continue
                html_sy = etree.HTML(sep_symptom.content)
                t = html_sy.xpath("//div[@class='article_paragraph']/p//text()")
                if len(t) > 0:
                    dict1['illness_symptom'] = ' '.join(t)

                sep_pathogen = requests.get(url_list[2], headers=self.headers)
                if sep_pathogen.status_code == 500:
                    print('urls+lsit[2]')
                    continue
                html_pa = etree.HTML(sep_pathogen.content)
                t_s = html_pa.xpath("//div[@class='article_paragraph']/p//text()")
                if len(t_s) > 0:
                    dict1['illness_pathogen'] = ' '.join(t_s)

                sep_complication = requests.get(url_list[3], headers=self.headers)
                if sep_complication.status_code == 500:
                    continue

                html_complication = etree.HTML(sep_complication.content)
                t_c = html_complication.xpath("//div[@class='disease_box']/div[2]//p/text()")
                if len(t_c) > 0:
                    dict1['illness_complication'] = ' '.join(t_c).replace('\r\n', '').replace(' ', '')

                sep_prevent = requests.get(url_list[4], headers=self.headers)
                if sep_prevent.status_code == 500:
                    continue

                html_pr = etree.HTML(sep_prevent.content)
                t_p = html_pr.xpath("//div[@class='article_box']//p/text()")
                if len(t_p) > 0:
                    dict1['illness_prevent'] = ' '.join(t_p)

                sep_identify = requests.get(url_list[5], headers=self.headers)
                if sep_identify.status_code == 500:
                    continue

                html_identify = etree.HTML(sep_identify.content)
                t_i = html_identify.xpath("//div[@class='article_box']//p/text()")
                if len(t_i) > 0:
                    dict1['illness_identify'] = ' '.join(t_i)

                sep_treat = requests.get(url_list[6], headers=self.headers)
                if sep_treat.status_code == 500:
                    continue

                html_treat = etree.HTML(sep_treat.content)
                t_t = html_treat.xpath("//div[@class='article_box']//p/text()")
                if len(t_t) > 0:
                    dict1['illness_treat'] = ' '.join(t_t)

                sep_see = requests.get(url_list[7], headers=self.headers)


                if sep_see.status_code == 500:
                    continue
                html_see = etree.HTML(sep_see.content)
                t_see = html_see.xpath("//div[@class='article_box']//p/text()")
                if len(t_see) > 0:
                    dict1['illness_see'] = ' '.join(t_see)



                sep_examine = requests.get(url_list[8], headers=self.headers)


                if sep_examine.status_code == 500:
                    continue
                html_examine = etree.HTML(sep_examine.content)
                t_examine = html_examine.xpath("//div[@class='article_box']//p/text()")
                if len(t_examine) > 0:
                    dict1['illness_examine'] = ' '.join(t_examine)

                sep_nurse = requests.get(url_list[9], headers=self.headers)


                if sep_nurse.status_code == 500:
                    continue
                html_nurse = etree.HTML(sep_nurse.content)
                t_nurse = html_nurse.xpath("//div[@class='article_box']//p/text()")
                if len(t_nurse) > 0:
                    dict1['illness_nurse'] = ' '.join(t_nurse)

                diet = requests.get(url_list[10], headers=self.headers)

                if diet.status_code == 500:
                    continue
                html_diet = etree.HTML(diet.content)
                t_diet = html_diet.xpath("//div[@class='article_box']//p/text()")
                if len(t_diet) > 0:
                    dict1['diet'] = ' '.join(t_diet)

                json_dict = json.dumps(dict1, ensure_ascii=False)

                with open('39jibing阶段1.json', 'a', encoding='utf-8')as f:
                    print(json_dict)
                    f.write(json_dict + ',' + '\n')
                # list2.append(dict1)

      except:
          pass

    # def save(self,list2):
    #     try:
    #         for k in list2:
    #             json_dict=json.dumps(k,ensure_ascii=False)
    #             with open('39jibing2.json','a',encoding='utf-8')as f:
    #                 f.write(json_dict+','+'\n')
    #     except:
    #         pass


    def run(self):
        try:

            list1=self.first_url()
            print(len(list1))
            for i in list1[39::]:
                print('这是科室的列表',i,list1.index(i))
                print(list1.index(i))

                self.send_url(i)
                # self.save(list2)
        except:
            pass

jbbk=JbBk()
jbbk.run()