import json
import requests
from lxml import etree
import random

# 15, 41610; 8726为界
# 开始20000
for i in range(22513,41610):
    # http://www.360jibing.com/l-2/2.html
    url = "http://www.360jibing.com/l-2/" + str(i) +".html"
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
        r = requests.get(url, headers=headers)
        r = r.content
        html = etree.HTML(r)

        url2_list = html.xpath('//*[@class="title"]/@href')
        # print(url2_list)

        for url2 in url2_list:
            print(url2)
            try:
                # url2 = "http://www.360jibing.com/question/view/618033.html"
                r2 = requests.get(url2, headers=headers)
                r2 = r2.content
                html2 = etree.HTML(r2)

                ask_dic = {}
                try:
                    questions_list = html2.xpath('//*[@id="question_content"]/cd/pre/p/text()')
                    # print(questions_list)
                    q = ""
                    q_a = questions_list[0]
                    if len(questions_list) > 1:
                        for question in questions_list:
                            q += question.strip().replace("健康咨询病史及病情描述：", "")\
                                .replace("希望医生或热心会员给予帮助：", "") + " "
                        # print(111, q[len(q_a):])
                        q = q[len(q_a):]
                    else:
                        q = questions_list[0]
                        # print(222,q)

                    if q != "":
                        ask_dic["question"] = q
                        try:
                            # answer_list = html2.xpath('//*[@id="best_answer_content"]/ca/pre/p//text()')
                            answer_list = html2.xpath('//*[@id="best_answer_content"]/ca/pre//text()')

                            # print(answer_list)
                            a = ""
                            for answer in answer_list:
                                # print(answer)
                                a += answer.strip().replace("疾病病情回顾分析：", "")\
                                    .replace("疾病病情回顾分析:", "")\
                                    .replace("疾病治疗方法及处理意见：", "")\
                                    .replace("疾病治疗方法及处理意见:", "") \
                                    .replace("，感谢您在360疾病网提问","")\
                                    .replace("感谢您在360疾病网提问", "")\
                                    .replace("在360疾病网","")\
                                    .replace("360疾病网( http://www.360jibing.com )","")\
                                    .replace("360疾病网","")\
                                    .replace("http://www.360jibing.com","")
                            # print(a)
                            if a != "":
                                ask_dic["answer"] = a

                                # print(ask_dic)
                                ask_dic_json = json.dumps(ask_dic, ensure_ascii=False)
                                print(ask_dic_json)
                                with open('./360jibing_ask.json', 'a+', encoding='utf-8') as f:
                                    f.writelines(ask_dic_json + ',' + '\n')
                            else:
                                print("answer为空")
                                with open('./kong_url.txt', 'a+', encoding='utf-8') as f1:
                                    f1.writelines(url2 + '\n')
                        except:
                            pass
                    else:
                        print("question为空")
                except:
                    print("出错url： %s" % url)
            except:
                print(url2)
    except:
        print(url)






