import re
import json
from lxml import etree
import requests
import time
import random

class Openration():
    def __init__(self):
        self.url='http://jbk.39.net/bw/t3_p11/'
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
             }
        # self.proxy_list = []
        # self.ke_proxy_list=[]

    def first_url(self):
      try:

        n=0

        url_lisst=[]
        while n<2:
                n+=1
                print(n,'页数')
                url='http://jbk.39.net/bw/t3_p{}/'.format(n)
                time.sleep(1)
                try:
                    sep=requests.get(url,headers=self.headers,timeout=5)


                except:
                    continue

                if sep.status_code==404:
                    continue
                if sep.status_code==500:
                    continue
                html=etree.HTML(sep.text)
                url_list=html.xpath("//*[@class='disease_box']/div/div/div/p/a/@href")
                url_lisst.append(url_list)
        print(url_lisst)

        return url_lisst
      except:
          pass
    def con_url(self,url):
        try:
                we=0
                for i in url[::]:
                    print(i,'次数')
                    we+=1
                    print(we)
                    dict1={}
                    try:
                        # proxies = random.choice(self.ipllist)
                        con_list=requests.get(i,headers=self.headers)
                    except:
                        continue
                    if con_list.status_code==404:
                        continue
                    if con_list.status_code==500:
                        continue
                    con_html = etree.HTML(con_list.text)
                    title = con_html.xpath("//*[@class='s_con clearfix']/article/div[1]/div[1]/h1/b//text()")
                    dict1['title'] = ''.join(title)

                    alias = con_html.xpath("//*[@class='s_con clearfix']/article/div[1]/div[1]/span//text()")
                    dict1['alias'] = ''.join(alias)
                    label = con_html.xpath("//*[@class='ss_det catalogItem']/div[2]/span//text()")
                    dict1['label'] = ' '.join(label).replace(' \r\n                                ', '').replace(
                        '\r\n                                         ', '').replace('\r\n                                 ','').replace('\r\n                        ','')

                    bao = i + 'baojia/'
                    try:
                        bao_sep = requests.get(bao, headers=self.headers)
                    except:
                        continue
                    if bao_sep.status_code == 404:
                        continue
                    if bao_sep.status_code == 500:
                        continue
                    bao_html = etree.HTML(bao_sep.text)
                    # introduce = bao_html.xpath("//*[@class='des']/p//text()")
                    introduce = bao_html.xpath("//*[@class='ss_det']/div[2]/div[1]/p/text()")
                    dict1['introdce'] = ''.join(introduce).replace('\u3000\u3000', '').replace('\xa0 \xa0 ', '')
                    list1 = []
                    for j in range(1, 7):
                        dict2 = {}
                        str_title = con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/b//text()".format(j))
                        if len(str_title) > 0:
                            str_con = con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/a/text()".format(j))
                            str_con = ' '.join(str_con).replace('\r\n                            ', '')
                            if len(str_con)==0:
                                #处理科室
                                print('处理科室')
                                str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/text()".format(j))
                                str_con = ''.join(str_con).replace('\r\n                            \r\n', '').replace(
                                    '\xa0\r\n                        ', '')
                            if '禁忌人群'in  str_title[0]:

                                str_con = con_html.xpath("//*[@class='infolist']/li[4]/span/cite/i/text()".format(j))
                                str_con=' '.join(str_con)
                                print(str_con)

                            if '相关疾病' in str_title[0]:
                                    #处理相关疾病
                                    str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/i/a/text()".format(j))
                                    if '更多' in str_con:
                                        str_con.remove('更多')
                                    str_con = ' '.join(str_con)
                            if '相关症状' in str_title[0]:
                                str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/i/a/text()".format(j))
                                if '更多' in str_con:
                                    str_con.remove('更多')
                                str_con = ' '.join(str_con)

                            if str_con == '查看详细>>':
                                #这个是价格
                                str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/i//text()".format(j))
                                if len(str_con) == 0:
                                    str_con = con_html.xpath(
                                        "//*[@class='info clearfix']/ul/li[{}]/span/i//text()".format(j))
                                str_con = ' '.join(str_con)
                            dict2[str_title[0]] = str_con

                            list1.append(dict2)

                        else:

                            str_title = con_html.xpath("//*[@class='long data']/div/b/text()")
                            str_title= ''.join(str_title)
                            if len(str_title)>0:

                                    str_list = []
                                    for we in range(1,4):
                                        dict_tit_ans={}

                                        str_biaoti = con_html.xpath(
                                            "//*[@class='long data']/div/dl[{}]/dt/text()".format(we))
                                        str_biaoti=''.join(str_biaoti)
                                        str_daan = con_html.xpath(
                                            "//*[@class='long data']/div/dl[{}]/dd/text()".format(we))
                                        str_daan=''.join(str_daan)
                                        dict_tit_ans[str_biaoti]=str_daan
                                        str_list.append(dict_tit_ans)
                                    dict2[str_title]=str_list
                            else:
                                break
                            list1.append(dict2)
                        dict1['basic_information']=list1
                        print(dict1)
                    list2 = []
                    for k in range(2, 9):
                        dict3 = {}
                        operation_title = con_html.xpath("//*[@class='w740']/div[{}]/div[1]/h3//text()".format(k))
                        operation_titles = ''.join(operation_title).replace('\r\n', '')
                        if len(operation_title)==0:
                            break
                        openration_con=con_html.xpath("//*[@class='w740']/div[{}]/div[2]/dl//text()".format(k)) and con_html.xpath("//*[@class='w740']/div[{}]/div[2]/p//text()".format(k)) or\
                                       con_html.xpath("//*[@class='w740']/div[{}]/div[2]/p//text()".format(k))or \
                                       con_html.xpath("//*[@class='w740']/div[{}]/div[2]/div/div/ul/li//text()".format(k))
                        openration_con = ' '.join( openration_con).replace('                                     ',' ')\
                                         .replace('                                 ',' ').replace('\r\n\r\n\r\n\r\n                                ',' ')
                        dict3[operation_titles] = openration_con
                        list2.append(dict3)
                        print(list2)
                        dict1['else_information'] = list2

                        if '包含项目' in operation_titles:

                            list3 = []
                            for x in range(2, 7):
                                # dict4 = {}
                                operation_url = \
                                    con_html.xpath("//*[@class='type_table']/table/tbody/tr[{}]/td[2]/a/@href".format(x))[0]

                                if len(operation_url) == 0:
                                    break
                                # openration_quote = con_html.xpath(
                                #     "//*[@class='lbox']/div/table/tbody/tr[{}]/td[3]//text()".format(x))
                                # dict4['openration_quote'] = ''.join(openration_quote).replace('\r\n', '').replace(
                                #     '\xa0 \xa0 ', '').replace('                                      ', '').replace(
                                #     '                 ', '').replace('              ','')
                                try:

                                    op_sep = requests.get(operation_url, headers=self.headers)
                                except:
                                    continue
                                if op_sep.status_code == 404:
                                    continue
                                if op_sep.status_code == 500:
                                    continue
                                #
                                op_html = etree.HTML(op_sep.text)

                                #

                                op_title = op_html.xpath(
                                    "//*[@class='s_con clearfix']/article/div[1]/div[1]/h1/b//text()")
                                dict1['title'] = ''.join(op_title)

                                alias = op_html.xpath(
                                    "//*[@class='s_con clearfix']/article/div[1]/div[1]/span//text()")

                                dict1['alias'] = ''.join(alias).replace('\r\n                                ', ' ')
                                label = op_html.xpath("//*[@class='ss_det catalogItem']/div[2]/span//text()")
                                dict1['label'] = ' '.join(label).replace(' \r\n                                ',
                                                                         '').replace(
                                    '\r\n                                         ', '')


                                list8 = []

                                for v in range(1, 7):
                                    dict6 = {}
                                    st_title = op_html.xpath(
                                        "//*[@class='info clearfix']/ul/li[{}]/span/b//text()".format(v))
                                    if len(st_title) > 0:
                                        st_con = op_html.xpath(
                                            "//*[@class='info clearfix']/ul/li[{}]/span/a/text()".format(v))
                                        st_con = ' '.join(st_con).replace('\r\n                            ', '')
                                        if len(st_con) == 0:
                                            # 处理科室
                                            print('处理科室')
                                            st_con = op_html.xpath(
                                                "//*[@class='infolist']/li[{}]/span/text()".format(v))
                                            st_con = ''.join(st_con).replace('\r\n                            \r\n',
                                                                               '').replace(
                                                '\xa0\r\n                        ', '')
                                        if '禁忌人群' in st_title[0]:
                                            st_con = op_html.xpath(
                                                "//*[@class='infolist']/li[4]/span/cite/i/text()".format(v))
                                            st_con = ' '.join(st_con)
                                            print(st_con)

                                        if '相关疾病' in st_title[0]:
                                            # 处理相关疾病
                                            st_con = op_html.xpath(
                                                "//*[@class='infolist']/li[{}]/span/i/a/text()".format(v))
                                            if '更多' in st_con:
                                                st_con.remove('更多')
                                            st_con = ' '.join(st_con)
                                        if '相关症状' in st_title[0]:
                                            st_con = op_html.xpath(
                                                "//*[@class='infolist']/li[{}]/span/i/a/text()".format(v))
                                            if '更多' in st_con:
                                                st_con.remove('更多')
                                            st_con = ' '.join(st_con)

                                        if st_con == '查看详细>>':
                                            # 这个是价格
                                            st_con = op_html.xpath(
                                                "//*[@class='infolist']/li[{}]/span/i//text()".format(v))
                                            if len(st_con) == 0:
                                                st_con = op_html.xpath(
                                                    "//*[@class='info clearfix']/ul/li[{}]/span/i//text()".format(v))
                                            st_con = ' '.join(st_con)

                                        dict6[st_title[0]] = st_con

                                        list8.append(dict6)

                                    else:

                                        st_title = op_html.xpath("//*[@class='long data']/div/b/text()")

                                        st_title = ''.join(st_title)
                                        if len(st_title) > 0:

                                            st_list = []
                                            for wer in range(1, 4):
                                                dict_tit_ans1 = {}

                                                st_biaoti = op_html.xpath(
                                                    "//*[@class='long data']/div/dl[{}]/dt/text()".format(wer))
                                                st_biaoti = ''.join(st_biaoti)
                                                st_daan = op_html.xpath(
                                                    "//*[@class='long data']/div/dl[{}]/dd/text()".format(wer))
                                                st_daan = ''.join(st_daan)
                                                dict_tit_ans1[st_biaoti] = st_daan
                                                print(dict_tit_ans1)
                                                st_list.append(dict_tit_ans1)
                                            dict6[st_title] = st_list
                                            print(dict6, 'jieudnabiaoz')
                                        else:
                                            break
                                        list8.append(dict6)
                                    dict1['basic_information'] = list8

                                list7=[]
                                for u in range(2, 9):
                                    dict9 = {}

                                    operation_title1 = op_html.xpath(
                                        "//*[@class='w740']/div[{}]/div[1]/h3//text()".format(u))
                                    operation_titles1 = ''.join(operation_title1).replace('\r\n', '')

                                    if len(operation_title1) == 0:
                                        break
                                    openration_con1 = op_html.xpath(
                                        "//*[@class='w740']/div[{}]/div[2]/dl//text()".format(
                                            u)) and op_html.xpath(
                                        "//*[@class='w740']/div[{}]/div[2]/p//text()".format(u)) or \
                                                     op_html.xpath(
                                                         "//*[@class='w740']/div[{}]/div[2]/p//text()".format(u)) or \
                                                     op_html.xpath(
                                                         "//*[@class='w740']/div[{}]/div[2]/div/div/ul/li//text()".format(
                                                             u))
                                    openration_con1 = ' '.join(openration_con1).replace(
                                        '                                     ', ' ') \
                                        .replace('                                 ', ' ').replace(
                                        '\r\n\r\n\r\n\r\n                                ', ' ')

                                    dict9[operation_titles1] = openration_con1
                                    list7.append(dict9)


                                dict1['basic_information'] = list8
                                dict1['else_information'] = list7
                                #
                                bao1 = operation_url + 'baojia/'
                                try:
                                    bao1_sep = requests.get(bao1, headers=self.headers)
                                except:
                                    continue
                                if bao1_sep.status_code == 404:
                                    continue
                                if bao1_sep.status_code == 500:
                                    continue

                                bao1_html = etree.HTML(bao1_sep.text)

                                introduce1 =bao1_html.xpath("//*[@class='ss_det']/div[2]/div[1]/p/text()")
                                dict1['introdce'] = ''.join(introduce1).replace('\u3000\u3000', '').replace(
                                    '\xa0 \xa0 ', '')
                                dict1['basic_information'] = list8
                                dict1['else_information'] = list7

                                # p_sep = requests.get(operation_url, headers=self.headers)

                                josn_dict1 = json.dumps(dict1, ensure_ascii=False)
                                print(josn_dict1)
                                with open('39检查.json', 'a', encoding='utf-8')as f:
                                    f.write(josn_dict1 + ',' + '\n')

                    josn_dict1 = json.dumps(dict1, ensure_ascii=False)
                    print(josn_dict1)
                    with open('39检查.json', 'a', encoding='utf-8')as f:
                        f.write(josn_dict1 + ',' + '\n')
        except:
            pass

    def run(self):
        url_list=self.first_url()
        for url in url_list:

            self.con_url(url)

openration=Openration()
openration.run()