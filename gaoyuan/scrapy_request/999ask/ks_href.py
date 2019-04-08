
import re
import json
import requests
from lxml import etree



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

# http://www.999ask.com
url = "http://www.999ask.com/list"
print(url)

r1 = requests.get(url, headers=headers)
r1 = r1.text
html1 = etree.HTML(r1)

li_href_list = html1.xpath('//*[@class="keshi_name"]/a/@href')
# print(li_href_list)

for li_href in li_href_list:
    url2 = "http://www.999ask.com" + li_href + "over/"
    print(url2)

    n_u = requests.get(url2, headers=headers)
    n_u = n_u.text
    ht = etree.HTML(n_u)
    n_u_list = ht.xpath('//*[@class="pagelist"]/a[11]/@href')
    if len(n_u_list) > 0:
        n = n_u_list[0]
        num1 = re.findall(r'\d+', n)[0]
        num = int(num1)
        # print(num)
    else:
        num = 1

    for i in range(1, num+1):
        url3 = url2 + str(i) +".html"
        print(url3)
        with open('./href_over.txt', 'a+', encoding='utf-8') as f:
            f.writelines(url3 + '\n')









