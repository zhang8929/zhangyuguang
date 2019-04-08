import json
import requests
from lxml import etree
import random



n = 0
for i in range(1833):
    n += 1
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

    # http://ask.bjhbyy.com/c-all/2/1.html
    url = "http://ask.bjhbyy.com/c-all/2/" + str(n) + ".html"

    r = requests.get(url, headers=headers)
    r = r.text
    html = etree.HTML(r)

    wt_href_list = html.xpath('//*[@class="w1100 content"]/div[1]/div[1]/div[2]/div[2]/ul/li/a/@href')

    # print(wt_href_list)
    for wt_href in wt_href_list:
        print(wt_href)

        with open('./bjyy_href.txt', 'a+', encoding='utf-8') as f:
            f.writelines(wt_href + '\n')
