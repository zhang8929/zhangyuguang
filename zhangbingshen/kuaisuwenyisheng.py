import requests
import json
from lxml import etree
import random
class KuaiSu():
    def __init__(self):
        self.url='http://yp.120ask.com/search/36.html'
        self.user_agent_list = [ "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" ,
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            'MQQBrowser/26Mozilla/5.0(Linux;U;Android2.3.7;zh-cn;MB200Build/GRJ22;CyanogenMod-7)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1',
            'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
        ]
        self.UserAgent = random.choice(self.user_agent_list)
        self.headers = {'User-Agent': self.UserAgent}
        # with open('pi_id','r')as f:
        #     list1=f.readlines()
        # list_ip = []
        # for ips in list1:
        #     ips=ips.replace('\n','')
        #     ips = ips.replace('\r', '')
        #
        #     proxie = { "https": "http://" + ips}
        #     try:
        #         response = requests.get('http://site.baidu.com/', proxies=proxie,  timeout=3).status_code
        #         print(response)
        #         if response == 200:
        #             list_ip.append(ips)
        #             continue
        #         if response !=200:
        #             continue
        #     except:
        #         pass
        #     ip = random.choice(list_ip)
        #     self.proxies = {"http": "http://" + ip}
        #     print(self.proxies)
    def first_url(self,ur):
        try:
            list1 = []
            print()
            urlw = ur.split('-')
            print(urlw)
            w = urlw[1].split('.')
            n=0
            while n < 200:
                n = n + 1
                url=urlw[0]+'-'+w[0]+'-'+str(n)+'--0-0-0-0'+'.'+'html'
                print(url)

                sep = requests.get(url,headers=self.headers,timeout=5)
                if sep ==None:
                  break
                if sep.status_code !=200:
                  continue

                html = etree.HTML(sep.text)
                urls = html.xpath("//div[@class='Sort-list Drug-store']/ul/li/a/@href")
                if len(urls)==0:
                    break
                print (urls)
                if len(urls) > 0:
                    list1.append(urls)


            return list1
        except:
            pass
    def sencent(self,i):

        for uy in i:
            try:
                urle = 'http://yp.120ask.com' + uy
                print(urle)

                sen_sep=requests.get(urle,headers=self.headers,timeout=5)


                sen_html=etree.HTML(sen_sep.text)

                dict1={}
                title=sen_html.xpath("//div[@class='details-left']/div[2]/p[1]//text()")

                print(title)
                title=''.join(title)
                dict1['title']=title
                dict1['url']=urle
                print(dict1,'????')


                list4=[]
                for ins in range(1,20):
                    dict3 = {}
                    title_in=sen_html.xpath("//div[@class='cont-1 tab-dm-1']//p[{}]/span//text()".format(ins))
                    title_in=''.join(title_in)
                    if len(title_in)==0:
                        break
                    con_in = sen_html.xpath("//div[@class='cont-1 tab-dm-1']//p[{}]/var//text()".format(ins))
                    con_in=''.join(con_in)
                    dict3[title_in]=con_in
                    list4.append(dict3)
                dict1['particulars']=list4


                list5=[]
                for int in range(1, 30):
                    dict4 = {}

                    title_int = sen_html.xpath("//div[@class='cont-2 tab-dm-2']//p[{}]/span//text()".format(int))
                    title_int = ''.join(title_int)

                    if len(title_int) == 0:
                        break
                    con_int = sen_html.xpath("//div[@class='cont-2 tab-dm-2']//p[{}]/var//text()".format(int))
                    con_int = ''.join(con_int)
                    dict4[title_int] = con_int
                    list5.append(dict4)

                dict1['specification'] = list5
                list2 = []
                for cos in range(1, 20):


                    dict2 = {}
                    co_title = sen_html.xpath("//div[@class='details-left']/div[2]/ul/li[{}]//text()".format(cos))

                    if len(co_title) == 0:
                        break
                    co_title=''.join(co_title).replace('\r\n                    ',' ')
                    print(co_title)

                    list2.append(co_title)

                dict1['basic_information'] = list2


                js_dict1=json.dumps(dict1,ensure_ascii=False)
                print(js_dict1)

                with open('kuaisu2.json','a',encoding='utf-8')as f:
                    f.write(js_dict1+','+'\n')

            except:
                pass




    def run(self):
        try:
            d='http://yp.120ask.com/search/.html'

            for r in range(1,100):
                d = 'http://yp.120ask.com/search/{}.html'.format(r)

                for s in range(1, 30):
                    d=d.split('/')
                    print(d)
                    f=d[len(d)-1].split('.')
                    print(f)
                    ur=d[0]+'//'+d[2]+'/'+d[3]+'/'+f[0]+'-'+str(s)+'.'+'html'
                    print(ur)
                    # ur = 'http://yp.120ask.com/search/36-{}.html'.format(s)

                    list1=self.first_url(ur)
                    if len(list1)==0:
                        break
                    print(list1)
                    for i in list1:

                        self.sencent(i)
        except:
            pass

kuai=KuaiSu()
kuai.run()


