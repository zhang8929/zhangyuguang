import requests
import json
from lxml import etree

class FeiHua():
    def __init__(self):
        self.url='https://dise.fh21.com.cn/department/illness/5.html'
        self.headers={'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1' }
    def frist_url(self):
        sep=requests.get(self.url,headers=self.headers)
        html=etree.HTML(sep.text)
        urls=html.xpath("//div[@class='menu_con']/dl/dd/ul/li/a/@href")
        print(len(urls))
        print(urls)
        return urls
    def send_url(self,i):
        i='https://dise.fh21.com.cn'+i
        sen_sep=requests.get(i,headers=self.headers)


        sen_html=etree.HTML(sen_sep.text)

        f_url=sen_html.xpath("//div[@class='dise_list']/ul[1]/li/a/@href")
        s_url=sen_html.xpath("//div[@class='dise_list']/ul[2]/li/a/@href")
        f_url.extend(s_url)

        return f_url
    def sends_url(self,i):
        w=i.split('/')
        t=w[3].split('.')
        n=0
        list2=[]
        try:
            while n<8:
                n+=1
                k='https://dise.fh21.com.cn'+'/'+w[1]+'/'+w[2]+'/'+t[0]+"-{}.html".format(n)

               # k='https://dise.fh21.com.cn/department/illness/5.html'

                sens_sep = requests.get(k, headers=self.headers)

                sens_html = etree.HTML(sens_sep.text)
                f_urls = sens_html.xpath("//div[@class='dise_list']/ul[4]/li/a/@href")
                if len(f_urls)==0:
                    break
                list2.append(f_urls)
        except:
            pass
        else:

             return list2
    def cend_url(self,j):
        for k in j :
            try:
                print(k)
                cend=requests.get(k,headers=self.headers)
                cend_html=etree.HTML(cend.text)
                dict1={}
                s=cend_html.xpath("//*[@class='main_content'][1]/ol/p/text()")[0]
                if len(s)>0:
                    dict1['title']=''.join(s)
                m=cend_html.xpath('//div[@class="dise03"]/dl[1]/dd//text()')
                if len(m)>0:
                    dict1['pathogenic_site']=''.join(m)

                q = cend_html.xpath('//div[@class="dise03"]/dl[2]/dd//text()')
                if len(q) > 0:
                    dict1['Clinical_Cente'] = ''.join(q)

                w = cend_html.xpath('//div[@class="dise03"]/dl[3]/dd/text()')
                if len(w) > 0:
                    dict1['classical_symptom'] = ''.join(w)

                p = cend_html.xpath('//div[@class="dise03"]/dl[4]/dd/text()')
                if len(p) > 0:
                    dict1['inspection_item'] = ''.join(p)

                z = cend_html.xpath('//div[@class="dise03"]/dl[5]/dd/text()')
                if len(z) > 0:
                    dict1['infectious'] = ''.join(z)

                x= cend_html.xpath('//div[@class="dise03"]/dl[6]/dd/text()')
                if len(x) > 0:
                    dict1['High-risk_groups'] = ''.join(x)

                ur=cend_html.xpath('//dd[@class="dise02b"]/p/a/@href')
                ur_con='https://dise.fh21.com.cn'+ur[0]
                con_ur=requests.get(ur_con,headers=self.headers)
                con_ur_html=etree.HTML(con_ur.text)

                sum =con_ur_html.xpath("//ul[@class='detailc']/p//text()")

                if len(sum)>0:
                    dict1['summarize']=''.join(sum)

                ur_con2='https://dise.fh21.com.cn'+ur[1]
                con_ur2=requests.get(ur_con2,headers=self.headers)
                con_ur_html2=etree.HTML(con_ur2.text)
                patho=con_ur_html2.xpath("//ul[@class='detailc']/p//text()")
                if len(patho)>0:
                    dict1['pathogenesis']=''.join(patho)

                ur_con3 = 'https://dise.fh21.com.cn' + ur[2]
                con_ur3 = requests.get(ur_con3, headers=self.headers)
                con_ur_html3 = etree.HTML(con_ur3.text)
                symptom = con_ur_html3.xpath("//ul[@class='detailc']/p//text()")
                if len(symptom) > 0:
                    dict1['symptom'] = ''.join(symptom)

                ur_con4 = 'https://dise.fh21.com.cn' + ur[3]
                con_ur4 = requests.get(ur_con4, headers=self.headers)
                con_ur_html4 = etree.HTML(con_ur4.text)
                examine = con_ur_html4.xpath("//ul[@class='detailc']/p//text()")
                if len(examine) > 0:
                    dict1['examine'] = ''.join(examine)

                ur_con5= 'https://dise.fh21.com.cn' + ur[4]
                con_ur5 = requests.get(ur_con5, headers=self.headers)
                con_ur_html5 = etree.HTML(con_ur5.text)
                cure = con_ur_html5.xpath("//ul[@class='detailc']/p//text()")
                if len(cure) > 0:
                    dict1['cure'] = ''.join(cure)

                ur_con6 = 'https://dise.fh21.com.cn' + ur[5]
                con_ur6 = requests.get(ur_con6, headers=self.headers)
                con_ur_html6 = etree.HTML(con_ur6.text)
                complication = con_ur_html6.xpath("//ul[@class='detailc']/p//text()")
                if len(symptom) > 0:
                    dict1['complication'] = ''.join(complication)

                ur_con7 = 'https://dise.fh21.com.cn' + ur[6]
                con_ur7 = requests.get(ur_con7, headers=self.headers)
                con_ur_html7 = etree.HTML(con_ur7.text)
                prevent = con_ur_html7.xpath("//ul[@class='detailc']/p//text()")
                if len(prevent ) > 0:
                    dict1['prevent '] = ''.join(prevent )

                ur_con8 = 'https://dise.fh21.com.cn' + ur[7]
                con_ur8 = requests.get(ur_con8, headers=self.headers)
                con_ur_html8 = etree.HTML(con_ur8.text)
                diet = con_ur_html8.xpath("//ul[@class='detailc']/p//text()")
                if len( diet) > 0:
                    dict1[' diet '] = ''.join( diet)

                j_dict=json.dumps(dict1,ensure_ascii=False)
                print(j_dict)
                with open('feihua1.json','a',encoding='utf-8',)as f:
                    f.write(j_dict+','+'\n')
            except:
                continue

    def run(self):
        urls=self.frist_url()
        for i in urls:
            try:
                f_url=self.send_url(i)
                list2=self.sends_url(i)
                list2.append(f_url)
                print(list2)
                print(len(list2))
                for j in list2:
                    self.cend_url(j)
            except:
                continue


frihua=FeiHua()
frihua.run()