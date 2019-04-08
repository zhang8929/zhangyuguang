import requests
from lxml import etree
import json
class FsGb():
    def __init__(self):
        self.url = 'http://www.ypfs.net/ask/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}

    def frist_url(self):
        try:
            sep = requests.get(self.url, headers=self.headers)
            html = etree.HTML(sep.content)
            f_url = html.xpath('//div[@class="DiseaseNav"]/ul/li/span/a/@href')

        except:
            pass
        else:
            return f_url

    def sed_url(self,next_urls):
        list4 = []
        try:
          n=1
          while n<4000:
                print(n)
                sed_sep = requests.get(next_urls, headers=self.headers)
                sed_html = etree.HTML(sed_sep.content)
                url_list = sed_html.xpath('*//td[@class="alltitle"]/a/@href')
                #next_url1 = sed_html.xpath('//*/a[@class="next"]/@href')

                n+=1
                next_urls = 'http://www.ypfs.net/ask/browser-1-0-page-{}.html'.format(n)
                print(next_urls)

                if url_list in list4 :
                    print('zhang')
                    break
                list4.append(url_list)


        except:
            pass

        else:
            return list4

    def con_url(self,list4):

            for g in list4:
                for z in g:
                    try:
                        con = requests.get(z, headers=self.headers)
                        con_html = etree.HTML(con.content)
                        item = {}
                        item['url'] = z
                        item['question'] = con_html.xpath('//div[@class="questBlockTitle"]/span/text()')[0]
                        item['describe'] = con_html.xpath('//div[@class="questionDesc"]/p/text()')[0]
                        m = con_html.xpath('//div[@class="AnswerContent"]/p//text()')
                        k = ''.join(m).replace('\u3000', '')
                        item['answer'] = k

                        json_item = json.dumps(item, ensure_ascii=False)
                        print(json_item)
                        with open('fsgb.json', 'a', encoding='utf-8') as  f:
                            f.write(json_item + ',' + '\n')


                    except:
                        pass

    def run(self):
        f_url = self.frist_url()
        for i in f_url:
            print(i)
            urls = self.url + i
            list4=self.sed_url(urls)
            self.con_url(list4)


fsgb = FsGb()
fsgb.run()