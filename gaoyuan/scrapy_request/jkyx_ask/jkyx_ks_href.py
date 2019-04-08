
import re
import json
import requests
from lxml import etree



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

# https://www.vodjk.com/ask/
url = "https://www.vodjk.com/ask/"

r1 = requests.get(url, headers=headers)
r1 = r1.text
html1 = etree.HTML(r1)

li_href_list = html1.xpath('//*[@class="departments"]/li/a/@href')
print(li_href_list)

for url2_href in li_href_list:
    url2 = "https://www.vodjk.com" + url2_href +""
    # print(222, url2)

    r2 = requests.get(url2, headers=headers)
    r2 = r2.text
    html2 = etree.HTML(r2)

    ks_href_list = html2.xpath('//*[@class="yslist_dq"]/dl[2]/dd/a/@href')
    # print(ks_href_list)

    for url3_href in ks_href_list[1:]:
        url3 = "https://www.vodjk.com" + url3_href +""
        print(333, url3)

        r3 = requests.get(url3, headers=headers)
        r3 = r3.text
        html3 = etree.HTML(r3)

        page_num = html3.xpath('//*[@id="pages"]/div/ul/li[7]/a/text()')
        # print(444, page_num)

        if len(page_num) > 0:
            num = page_num[0]
            num = int(num)
            # print(num)
        else:
            num = 1

        for n in range(1, num+1):
            url4 = url3[0:-2] + str(n) + "/"
            print(555, url4)

            with open('./jkyx_ks_href.txt', 'a+', encoding='utf-8') as f:
                f.writelines(url4 + '\n')


