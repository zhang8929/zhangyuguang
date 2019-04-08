import re
import json
from lxml import etree
import requests
import time

class Openration():
    def __init__(self):
        self.url='http://jbk.39.net/bw/t4_p1/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    def first_url(self):
      try:
        n=8
        while n<88:
                n+=1
                print(n,'页数')
                url='http://jbk.39.net/bw/t4_p{}/'.format(n)
                time.sleep(2)
                sep=requests.get(url,headers=self.headers)

                html=etree.HTML(sep.text)

                url_list=html.xpath("//*[@class='disease_box']/div/div/div/p/a/@href")

                for i in url_list[5::]:

                    print(i,'次数')
                    dict1={}
                    time.sleep(2)
                    con_list=requests.get(i,headers=self.headers)

                    con_html=etree.HTML(con_list.text)
                    title=con_html.xpath("//*[@class='s_con clearfix']/article/div[1]/div[1]/h1/b//text()")
                    dict1['title']=''.join(title)

                    alias = con_html.xpath("//*[@class='s_con clearfix']/article/div[1]/div[1]/span//text()")
                    dict1['alias'] = ''.join(alias)
                    label=con_html.xpath("//*[@class='ss_det catalogItem']/div[2]/span//text()")
                    dict1['label']=' '.join(label).replace(' \r\n                                ','').replace('\r\n                                         ','')


                    list1=[]
                    for j in range(1,7):
                        dict2={}
                        str_title=con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/b//text()".format(j))

                        if len(str_title)>0:
                            str_con=con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/a/text()".format(j))

                            str_con=''.join(str_con).replace('\r\n                            ','')

                            if len(str_con)==0:
                                str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/text()".format(j))
                                str_con=''.join(str_con).replace('\r\n                            \r\n','').replace('\xa0\r\n                        ','')


                                if str_con=='\r\n                            \r\n                        ':
                                    str_con=con_html.xpath("//*[@class='long last']/span/i/a//text()")
                                    if '更多' in str_con:
                                        str_con.remove('更多')
                                    str_con=' '.join(str_con)

                            if str_con == '查看详细>>':
                                str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/i/text()".format(j))
                                if len(str_con)==0:
                                    str_con = con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/i//text()".format(j))
                                str_con = ' '.join(str_con)
                                print(str_con, '总')
                            dict2[str_title[0]] = str_con

                            list1.append(dict2)

                        else:
                            break

                    list2=[]
                    for k in range(2,9):
                        dict3={}
                        operation_title=con_html.xpath("//*[@class='w740']/div[{}]/div[1]/h3//text()".format(k))
                        operation_titles=''.join(operation_title).replace('\r\n','')

                        if len(operation_title)==0:
                            break
                        # operation_con= con_html.xpath("//*[@class='w740']/div[{}]/div[2]//text()".format(k))
                        operation_con = con_html.xpath("//*[@class='w740']/div[{}]/div//text()".format(k))
                        openration_con=''.join(operation_con[2::]).replace('\r\n',' ').replace('\u3000\u3000','').replace('                                      ','').replace('        文      ','').replace('        文图      ','')\
                            .replace('                                     ',' ').replace('                             ','').replace('                        ','').replace('                 ','')
                        # if '手术报价' in openration_con:


                        if len(openration_con)==0:
                                operation_con = con_html.xpath("//*[@class='text_item']/ul/li//text()")
                                openration_con = ''.join(operation_con).replace('\r\n','').replace('\u3000\u3000','').replace('                                                              ','').replace('                                      ','')\
                                    .replace('        文      ','').replace('        文图      ','').replace('                                     ',' ').replace('                             ','')\
                                    .replace('                        ','').replace('                 ','')
                                if len(openration_con)==0:
                                    operation_con = con_html.xpath("//*[@class='con clearfix']/ul/li//text()")
                                    openration_con = ''.join(operation_con).replace('\r\n',' ').replace('\u3000\u3000','').replace('                                     ','').replace('                                      ','').replace('                        ','')


                        dict3[operation_titles]=openration_con
                        list2.append(dict3)

                        bao = i + 'baojia/'
                        bao_sep = requests.get(bao, headers=self.headers)
                        bao_html = etree.HTML(bao_sep.text)
                        introduce = bao_html.xpath("//*[@class='des']/p//text()")
                        # introduce =con_html.xpath("//*[@class='ss_det catalogItem']/div[3]/span/p//text()")
                        dict1['introdce'] = ''.join(introduce).replace('\u3000\u3000', '').replace('\xa0 \xa0 ', '')
                        dict1['basic_information'] = list1
                        dict1['else_information'] = list2


                        con_list3= requests.get(i, headers=self.headers)
                        if '手术类别' in operation_titles:

                            list3=[]
                            for x in range(2,5):
                                        # dict4 = {}
                                        operation_url= con_html.xpath("//*[@class='lbox']/div/table/tbody/tr[{}]/td[2]/a/@href".format(x))[0]


                                        if len(operation_url)==0:

                                            break
                                        # openration_quote = con_html.xpath(
                                        #     "//*[@class='lbox']/div/table/tbody/tr[{}]/td[3]//text()".format(x))
                                        # dict4['openration_quote'] = ''.join(openration_quote).replace('\r\n', '').replace(
                                        #     '\xa0 \xa0 ', '').replace('                                      ', '').replace(
                                        #     '                 ', '').replace('              ','')

                                        op_sep=requests.get(operation_url,headers=self.headers)

                                        #
                                        op_html=etree.HTML(op_sep.text)

                                        #

                                        op_title = op_html.xpath(
                                            "//*[@class='s_con clearfix']/article/div[1]/div[1]/h1/b//text()")
                                        dict1['title'] = ''.join(op_title)

                                        alias = op_html.xpath(
                                            "//*[@class='s_con clearfix']/article/div[1]/div[1]/span//text()")

                                        dict1['alias'] = ''.join(alias).replace('\r\n                                ',' ')
                                        label = op_html.xpath("//*[@class='ss_det catalogItem']/div[2]/span//text()")
                                        dict1['label'] = ' '.join(label).replace(' \r\n                                ', '').replace('\r\n                                         ','')

                                        list8=[]

                                        for v in range(1, 7):
                                            dict5={}

                                            st_title = op_html.xpath("//*[@class='infolist']/li[{}]/span/b//text()".format(v))
                                            if len(st_title) > 0:
                                                str_c = op_html.xpath(
                                                    "//*[@class='infolist']/li[{}]/span/a/text()".format(v))
                                                str_c = ''.join(str_c).replace('\r\n                            ', '')


                                                if len(str_c) == 0:
                                                    str_c = op_html.xpath(
                                                        "//*[@class='infolist']/li[{}]/span/text()".format(v))
                                                    str_c = ''.join(str_c).replace('\r\n                            \r\n',
                                                                                       '').replace(
                                                        '\xa0\r\n                        ', '')


                                                    if str_c == '\r\n                            \r\n                        ':
                                                        str_c = op_html.xpath("//*[@class='long last']/span/i/a//text()")
                                                        if '更多' in str_c:
                                                            str_c.remove('更多')
                                                        str_c = ' '.join(str_c)

                                                if str_c == '查看详细>>':
                                                    str_c = op_html.xpath(
                                                        "//*[@class='info clearfix']/ul/li[{}]/span/i//text()".format(v))
                                                    # if len(str_c)==0:
                                                    #     str_c = con_html.xpath(
                                                    #         "//*[@class='long']/span/i//text()".format(
                                                    #             v))

                                                    str_c = ' '.join(str_c)


                                                dict5[st_title[0]] = str_c

                                                list8.append(dict5)
                                                dict1['basic_information'] = list8
                                            else:
                                                 break
                                        list7= []
                                        for u in range(2, 9):
                                            dict9 = {}
                                            operat_title = op_html.xpath(
                                                "//*[@class='w740']/div[{}]/div[1]/h3//text()".format(u))

                                            operat_titles = ''.join(operat_title).replace('\r\n', '').replace(                                                '                                      ', '')

                                            if len(operat_titles) == 0:
                                                break
                                            # operation_con= con_html.xpath("//*[@class='w740']/div[{}]/div[2]//text()".format(k))
                                            operat_con = op_html.xpath(
                                                "//*[@class='w740']/div[{}]/div//text()".format(u))
                                            openrat_con = ''.join(operat_con[2::]).replace('\r\n', ' ').replace(
                                                '\u3000\u3000', '').replace('                                      ',
                                                                            '').replace('        文      ', '').replace(
                                                '        文图      ', '') \
                                                .replace('                                     ', ' ').replace(
                                                '                             ', '').replace('                        ',
                                                                                             '').replace(
                                                '                 ', '')
                                            # if '手术报价' in openration_con:


                                            if len(openrat_con) == 0:
                                                operat_con = op_html.xpath("//*[@class='text_item']/ul/li//text()")
                                                openrat_con = ''.join(operat_con).replace('\r\n', '').replace(
                                                    '\u3000\u3000', '').replace(
                                                    '                                                              ',
                                                    '').replace('                                      ', '') \
                                                    .replace('        文      ', '').replace('        文图      ',
                                                                                            '').replace(
                                                    '                                     ', ' ').replace(
                                                    '                             ', '') \
                                                    .replace('                        ', '').replace(
                                                    '                 ', '')
                                                if len(openrat_con) == 0:
                                                    operat_con = op_html.xpath(
                                                        "//*[@class='con clearfix']/ul/li//text()")
                                                    openrat_con = ''.join(operat_con).replace('\r\n',
                                                                                                    ' ').replace(
                                                        '\u3000\u3000', '').replace(
                                                        '                                     ', '').replace(
                                                        '                                      ', '').replace(
                                                        '                        ', '')

                                            dict9[operat_titles] = openrat_con

                                            list7.append(dict9)

                                        dict1['basic_information'] = list8
                                        dict1['else_information'] = list7
                                        #
                                        bao1 = operation_url + 'baojia/'

                                        bao1_sep = requests.get(bao1, headers=self.headers)

                                        bao1_html = etree.HTML(bao1_sep.text)

                                        introduce1 = bao1_html.xpath("//*[@class='des']/p//text()")

                                        # introduce =con_html.xpath("//*[@class='ss_det catalogItem']/div[3]/span/p//text()")
                                        dict1['introdce'] = ''.join(introduce1).replace('\u3000\u3000', '').replace(
                                            '\xa0 \xa0 ', '')

                                        p_sep = requests.get(operation_url, headers=self.headers)

                                        josn_dict1 = json.dumps(dict1, ensure_ascii=False)

                                        with open('39shoushu.json', 'a', encoding='utf-8')as f:
                                            f.write(josn_dict1 + ',' + '\n')

                    title = con_html.xpath("//*[@class='s_con clearfix']/article/div[1]/div[1]/h1/b//text()")
                    dict1['title'] = ''.join(title)
                    josn_dict1=json.dumps(dict1,ensure_ascii=False)
                    print(josn_dict1)
                    alias = con_html.xpath("//*[@class='s_con clearfix']/article/div[1]/div[1]/span//text()")
                    dict1['alias'] = ''.join(alias)
                    label = con_html.xpath("//*[@class='ss_det catalogItem']/div[2]/span//text()")
                    dict1['label'] = ' '.join(label).replace(' \r\n                                ', '').replace(
                        '\r\n                                         ', '')

                    list1 = []
                    for j in range(1, 7):
                        dict2 = {}
                        str_title = con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/b//text()".format(j))

                        if len(str_title) > 0:
                            str_con = con_html.xpath("//*[@class='info clearfix']/ul/li[{}]/span/a/text()".format(j))
                            print(str_con,'vubf')
                            str_con = ''.join(str_con).replace('\r\n                            ', '')

                            if len(str_con) == 0:
                                str_con = con_html.xpath("//*[@class='infolist']/li[{}]/span/text()".format(j))
                                str_con = ''.join(str_con).replace('\r\n                            \r\n', '').replace(
                                    '\xa0\r\n                        ', '')

                                if str_con == '\r\n                            \r\n                        ':
                                    str_con = con_html.xpath("//*[@class='long last']/span/i/a//text()")
                                    if '更多' in str_con:
                                        str_con.remove('更多')
                                    str_con = ' '.join(str_con)

                            if str_con == '查看详细>>':
                                    str_con = con_html.xpath(
                                        "//*[@class='info clearfix']/ul/li[{}]/span/i//text()".format(j))
                                    str_con=''.join(str_con)
                            dict2[str_title[0]] = str_con

                            list1.append(dict2)

                        else:
                            break

                    list2 = []
                    for k in range(2, 9):
                        dict3 = {}
                        operation_title = con_html.xpath("//*[@class='w740']/div[{}]/div[1]/h3//text()".format(k))
                        operation_titles = ''.join(operation_title).replace('\r\n', '')
                        if '手术类别' in operation_titles:
                            continue

                        if len(operation_title) == 0:
                            break
                        # operation_con= con_html.xpath("//*[@class='w740']/div[{}]/div[2]//text()".format(k))
                        operation_con = con_html.xpath("//*[@class='w740']/div[{}]/div//text()".format(k))
                        openration_con = ''.join(operation_con[2::]).replace('\r\n', ' ').replace('\u3000\u3000',
                                                                                                  '').replace(
                            '                                      ', '').replace('        文      ', '').replace(
                            '        文图      ', '') \
                            .replace('                                     ', ' ').replace(
                            '                             ', '').replace('                        ', '').replace(
                            '                 ', '')
                        # if '手术报价' in openration_con:

                        print(len(openration_con))
                        if len(openration_con) == 0:
                            operation_con = con_html.xpath("//*[@class='text_item']/ul/li//text()")
                            openration_con = ''.join(operation_con).replace('\r\n', '').replace('\u3000\u3000',
                                                                                                '').replace(
                                '                                                              ', '').replace(
                                '                                      ', '') \
                                .replace('        文      ', '').replace('        文图      ', '').replace(
                                '                                     ', ' ').replace('                             ',
                                                                                      '') \
                                .replace('                        ', '').replace('                 ', '')
                            if len(openration_con) == 0:
                                operation_con = con_html.xpath("//*[@class='con clearfix']/ul/li//text()")
                                openration_con = ''.join(operation_con).replace('\r\n', ' ').replace('\u3000\u3000',
                                                                                                     '').replace(
                                    '                                     ', '').replace(
                                    '                                      ', '').replace('                        ',
                                                                                          '')

                        dict3[operation_titles] = openration_con

                        list2.append(dict3)

                    bao = i + 'baojia/'
                    bao_sep = requests.get(bao, headers=self.headers)
                    bao_html = etree.HTML(bao_sep.text)
                    introduce = bao_html.xpath("//*[@class='des']/p//text()")
                    # introduce =con_html.xpath("//*[@class='ss_det catalogItem']/div[3]/span/p//text()")
                    dict1['introdce'] = ''.join(introduce).replace('\u3000\u3000', '').replace('\xa0 \xa0 ', '')
                    dict1['basic_information'] = list1
                    print(dict1['basic_information'],'vrfffffeee')
                    dict1['else_information'] = list2
                    print(dict1, 'nizhendeee')


                    josn_dict1 = json.dumps(dict1, ensure_ascii=False)
                    with open('39shoushu.json','a',encoding='utf-8')as f:
                        f.write(josn_dict1+','+'\n')

      except:
          pass


    def run(self):
        self.first_url()

openration=Openration()
openration.run()