
import requests
import json
from lxml import etree
import random


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

url = "https://www.bohe.cn/ask/"
r = requests.get(url, headers=headers)
r = r.text
html = etree.HTML(r)

title_href_list = html.xpath('//*[@class="si-list"]/div/a/@href')
print(title_href_list)
# 93
# print(len(title_list))

for url2 in title_href_list:
    print(url2)

    r2 = requests.get(url2, headers=headers)
    r2 = r2.text
    # print(r2)
    html2 = etree.HTML(r2)
    try:
        num = html2.xpath('//*[@class="iask-pages-p"]/p/a[5]/text()')
        # print(num)
        if len(num) > 0:
            n = int(num[0])
            print(n, type(n))
            if n > 100:
                n = 100
            for i in range(1, n+1):
                u = url2[0:-5]
                url3 = (u + "-{}" + ".html").format(i)
                print(url3)
                with open('./bhys_href.txt', 'a+', encoding='utf-8') as f:
                    f.writelines(url3 + '\n')
        else:
            with open('./bhys_href.txt', 'a+', encoding='utf-8') as f:
                f.writelines(url2 + '\n')
    except:
        pass


