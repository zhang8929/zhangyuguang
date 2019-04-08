# -*- coding: utf-8 -*-
import scrapy

with open('./bk.json', 'r') as f:
    content = f.read().splitlines()

class XxwySpider(scrapy.Spider):
    name = 'xxwy'
    allowed_domains = ['jib.xywy.com']
    start_urls = ['http://jib.xywy.com/']



    def parse(self, response):

        # with open('./bk.json', 'r') as f:
        #     content = f.read().splitlines()
            for i in content:
                node1 = 'http://jib.xywy.com' + i

                # print(node2)
                temp = {}
                temp['link'] = node1
            # print(self.lis1)


                yield scrapy.Request(url=node1,callback=self.next1,meta={'temp':temp})
    def next1(self,response):

        temp = response.meta['temp']

        node2 = (response.url).replace('il_sii_', 'il_sii/gaishu/')

        yield scrapy.Request(url=node2,callback=self.next2,meta={'temp':temp})





    def next2(self,response):#概述页

        print(response.url)
        temp = {}

        temp['url'] = response.url
        # print(response.url)
        # temp['sick_name'] = response.xpath
        # temp = {}
        temp['sick_name'] = response.xpath('//*[@class="jb-name fYaHei gre"]/text()').extract_first()

        sick_introduce = response.xpath('//*[@class="jib-articl-con jib-lh-articl"]/p/text()').extract_first()

        temp['sick_introduce'] = (sick_introduce).strip()
        a = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[1]/span[1]/text()').extract_first()
        a = a.replace('：','')
        a_1 = response.xpath('//*[@class="jib-janj bor'
                             ' clearfix"]/div[2]/div[2]/p[1]/span[2]/text()').extract_first()
        a_1 = ((''.join(a_1)).replace('\n','')).strip()
        temp[a] = a_1

        b = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[2]/span[1]/text()').extract_first()
        b = b.replace('：', '')
        b_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[2]/span[2]/text()').extract_first()

        temp[b] = b_1

        c = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[3]/span[1]/text()').extract_first()
        c = c.replace('：', '')
        c_1 = response.xpath('//*[@class="jib-janj bor'
                             ' clearfix"]/div[2]/div[2]/p[3]/span[2]/text()').extract_first()
        c_1 = ((''.join(c_1)).replace('\n', '')).strip()
        temp[c] = c_1

        d = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[4]/span[1]/text()').extract_first()
        d = d.replace('：', '')
        d_1 = response.xpath('//*[@class="jib-janj bor'
                             ' clearfix"]/div[2]/div[2]/p[4]/span[2]/text()').extract()
        # d_1 = ((''.join(d_1)).replace('\n', '')).strip()
        temp[d] = d_1

        e = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[5]/span[1]/text()').extract_first()
        e = e.replace('：', '')
        e_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]/p[5]/span[2]/a/text()').extract()
        # e_1 = ((''.join(e_1)).replace('\n', '')).strip()
        temp[e] = e_1

        f = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[1]/span[1]/text()').extract_first()
        f = f.replace('：', '')
        f_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[1]/span[2]/text()').extract()
        # e_1 = ((''.join(e_1)).replace('\n', '')).strip()
        temp[f] =f_1

        g = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[2]/span[1]/text()').extract_first()
        g = g.replace('：', '')
        g_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[2]/span[2]/text()').extract()
        # e_1 = ((''.join(e_1)).replace('\n', '')).strip()
        temp[g] = g_1

        h = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[3]/span[1]/text()').extract_first()
        h = h.replace('：', '')
        h_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[3]/span[2]/text()').extract()
        h_1 = ((''.join(h_1)).replace('\n', '')).strip()
        temp[h] = h_1

        i = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[4]/span[1]/text()').extract_first()
        i = i.replace('：', '')
        i_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[4]/span[2]/text()').extract()
        i_1 = ((''.join(i_1)).replace('\n', '')).strip()
        temp[i] = i_1



        j = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[5]/span[1]/text()').extract_first()
        j = j.replace('：', '')
        j_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[5]/span[2]/a/text()').extract()
        # j_1 = ((''.join(j_1)).replace('\n', '')).strip()
        temp[j] = j_1

        k = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[6]/span[1]/text()').extract_first()
        if k != None:

            k = k.replace('：', '')
            k_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[3]/p[6]/span[2]/text()').extract()
            k_1 = ((''.join(k_1)).replace('\n', '')).strip()
            if k_1 ==[]:
                k_1='根据不同医院，收费标准不一致'

            temp[k] = k_1




        l = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[4]/strong[1]/text()').extract_first()

        l_1 = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[4]/p[1]/text()').extract()

        l_1 = ((''.join(l_1)).strip())



        temp[l] = l_1

        link = (response.url).replace('gaishu','cause')

        yield scrapy.Request(url=link,callback=self.next3,meta={'temp':temp})

    def next3(self,response):
        temp = response.meta['temp']
        a = (''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p[2]/text()').extract())).strip()
        if a =='':
            b = (''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p[3]/text()').extract())).strip()
            temp['病因'] = b
        else:
            temp['病因'] = a

        temp['发病机制'] = (''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p[3]//text()').extract())).strip()


        link = (response.url).replace('cause','prevent')
        yield scrapy.Request(url=link,callback=self.next4,meta={'temp':temp})

    def next4(self,response):
        temp = response.meta['temp']

        temp['预防'] = (((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p/text()').extract())).strip()).replace('\t','')).replace('\r\n','')


        link = (response.url).replace('prevent','neopathy')

        yield scrapy.Request(url=link,callback=self.next5,meta={'temp':temp})

    def next5(self,response):

        temp = response.meta['temp']

        temp['并发症content'] = ((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p//text()').extract())).strip()).replace('\t','')

        link = (response.url).replace('neopathy','symptom')

        yield scrapy.Request(url=link,callback=self.next6,meta={'temp':temp})

    def next6(self,response):

        temp = response.meta['temp']

        temp['症状'] = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/span/a/text()').extract()

        temp['症状content'] = (((((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]//text()').extract())).strip()).replace('\r\n','')).replace('\n','')).replace(' ','')).replace('\t','')


        link = (response.url).replace('symptom','inspect')

        yield scrapy.Request(url=link,callback=self.next7,meta={'temp':temp})

    def next7(self,response):

        temp = response.meta['temp']
        temp['检查项目'] = response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div/ul/li[1]/a/text()').extract()

        temp['检查content'] = ((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p/text()').extract())).strip()).replace('\t','')


        link = (response.url).replace('inspect','diagnosis')

        yield scrapy.Request(url=link,callback=self.next8,meta={'temp':temp})

    def next8(self,response):
        temp = response.meta['temp']

        temp['诊断鉴别'] = (((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]//p//text()').extract())).replace('\r\n','')).strip()).replace('\t','')

        link = (response.url).replace('diagnosis','treat')

        yield scrapy.Request(url=link,callback=self.next9,meta={'temp':temp})

    def next9(self,response):

        temp = response.meta['temp']

        temp['治疗content'] = (((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/div[2]//text()').extract())).replace('\r\n','')).strip()).replace('\t','')

        link = response.url.replace('treat','nursing')

        yield scrapy.Request(url=link,callback=self.next10,meta={'temp':temp})

    def next10(self,response):

        temp = response.meta['temp']

        temp['护理content'] = (((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]/p/text()').extract())).replace('\t','')).strip()).replace('\r\n','')

        # print(response.url)

        link = (response.url).replace('nursing','food')

        yield scrapy.Request(url=link,callback=self.next11,meta={'temp':temp})

    def next11(self,response):

        temp = response.meta['temp']

        temp['食疗方'] = ((((((''.join(response.xpath('//*[@class="jib-janj bor clearfix"]/div[2]//text()').extract())).replace('\r\n','')).strip()).replace('\n','')).replace(' ','')).strip()).replace('\t','')

        temp['宜食'] = response.xpath('//*[@class="diet-item none clearfix"]//p/text()').extract()

        temp['忌食'] = response.xpath('//*[@class="diet-item none"]//p/text()').extract()
        # print(self.lis2 + ('*'*100))
        #
        # print(self.lis1+'*'*1000)
        # if temp['sick_name'] ==
        yield temp
    #     # print(temp)
    # #     print(response.url)

    #

