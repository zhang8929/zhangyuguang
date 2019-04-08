import random
import re
import json
import requests
from lxml import etree


for i in range(1, 1060):
    # http://www.sh12320.com/c-all/1/1.html (22, 1060)
    # http://www.sh12320.com/c-all/2/1.html (22, 822)
    # url = "http://www.sh12320.com/c-all/1/{}.html".format(i)
    url = "http://www.sh12320.com/c-all/2/{}.html".format(i)

    print(url)

    user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                       "Chrome/22.0.1207.1 Safari/537.1",
                       "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) "
                       "Chrome/20.0.1132.57 Safari/536.11",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) "
                       "Chrome/20.0.1092.0 Safari/536.6",
                       "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) "
                       "Chrome/20.0.1090.0 Safari/536.6",
                       "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                       "Chrome/19.77.34.5 Safari/537.1",
                       "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) "
                       "Chrome/19.0.1084.9 Safari/536.5",
                       "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) "
                       "Chrome/19.0.1084.36 Safari/536.5",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1063.0 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1063.0 Safari/536.3",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1063.0 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1062.0 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1062.0 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1061.1 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1061.1 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1061.1 Safari/536.3",
                       "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
                       "Chrome/19.0.1061.0 Safari/536.3",
                       "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) "
                       "Chrome/19.0.1055.1 Safari/535.24",
                       "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
                       "Chrome/19.0.1055.1 Safari/535.24",
                       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                       "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                       "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                       "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                       "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                       "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                       "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                       "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                       "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
                       "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
                       "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                       "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                       "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
                       "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                       "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                       "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                       "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                       "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                       "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
                       "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
                       ]
    USER_AGENT = (random.sample(user_agent_list, 1))[0]
    headers = {'User-Agent': USER_AGENT}
    try:
        r1 = requests.get(url, headers=headers)
        r1 = r1.text
        html1 = etree.HTML(r1)

        li_href_list = html1.xpath('//*[@class="wrap"]/a/@href')
        print(li_href_list)

        for url2 in li_href_list:
            data_dic = {}
            # url2 = "http://wenda.viptijian.com{}".format(url_href)
            print(url2)
            try:
                r2 = requests.get(url2, headers=headers)
                r2 = r2.text
                html2 = etree.HTML(r2)

                questions_list = html2.xpath('//*[@class="questionbox"]/div[@class="description clearfix"]/p/text()')
                # print(questions_list)
                ask_dic = {}
                for question in questions_list:
                    q = question.strip().replace('"', '').replace('\n', '').replace('\r', '')
                    ask_dic["question"] = q
                # print("qqqqqq", q)

                if len(questions_list) != 0:
                    try:
                        a = ""
                        # http://www.sh12320.com/c-all/1/1.html（未解决页）
                        answer_list = html2.xpath('//*[@id="comment_0"]/div[1]/div[2]/p/text()')

                        # http://www.sh12320.com/c-all/2/1.html（已解决页）
                        # answer_list = html2.xpath('//*[@class="qa-content"]/p/text()')
                        # print(answer_list)
                        for answer in answer_list:
                            a += answer.strip().replace('"', '')\
                                .replace('\n', '').replace('\r', '')\
                                .replace('病情分析：', '').replace('指导意见：', '')
                        # ask_dic["answer"] = a
                        print("aaaaaa", a)
                        if len(answer_list) != 0:
                            ask_dic_json = json.dumps(ask_dic, ensure_ascii=False)
                            print(ask_dic_json)
                            with open('./hys_ask.json', 'a+', encoding='utf-8') as f:
                                f.writelines(ask_dic_json + ',' + '\n')
                        else:
                            print("answer为空")
                    except:
                        print("Error", url2)
                else:
                    print("question为空")
            except:
                print("Error:", url2)
    except:
        print("Error:", url)




