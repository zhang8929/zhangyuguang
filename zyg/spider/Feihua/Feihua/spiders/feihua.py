# -*- coding: utf-8 -*-
import scrapy

with open('./url.json','r')as f:
    content = f.read().splitlines()
    # print(content)
class FeihuaSpider(scrapy.Spider):
    name = 'feihua'
    # allowed_domains = ['zz.qm120.com/']
    start_urls = ['http://zz.qm120.com/']

    def parse(self, response):
        link = response.url

        yield scrapy.Request(url=link,callback=self.next1)


    def next1(self,response):
        for i in content:
            # print(i)
            link = 'http://zz.qm120.com' + i
            # print(link)

            yield scrapy.Request(url=link,callback=self.next2,dont_filter=True)


    def next2(self,response):

        temp ={}

        temp['症状名称'] = response.xpath('/html/body/div[5]/div[1]/div[2]/ul/li[1]/span[1]/text()').extract_first()

        temp['症状部位'] = response.xpath('/html/body/div[5]/div[1]/div[2]/ul/li[1]/span[2]/a/text()').extract_first()


        temp['症状科室'] = response.xpath('/html/body/div[5]/div[1]/div[2]/ul/li[2]/span/a/text()').extract()

        temp['症状介绍'] = response.xpath('/html/body/div[5]/div[1]/div[3]/text()').extract_first()

        temp['相关疾病'] = response.xpath('/html/body/div[5]/div[1]/div[5]/div[2]/ul/li/a/text()').extract()

        temp['url'] = response.url

        a = response.url.replace('g/','g/bingyin_')
        # print(a)
        yield scrapy.Request(url=a,callback=self.next3,meta={'temp':temp})

    def next3(self,response):
        temp = response.meta['temp']

        a = response.xpath('/html/body/div[5]/div[1]/div[2]//text()').extract()

        a1 = ((''.join(a)).replace('\r\n\t','')).strip()

        temp['病因'] = a1

        # print(temp['url'])

        link = (temp['url']).replace('g/','g/jiancha_')
        print(link)

        yield scrapy.Request(url=link,callback=self.next4,meta={'temp':temp})

    def next4(self,response):

        temp = response.meta['temp']

        temp['检查'] = ((''.join(response.xpath('/html/body/div[5]/div[1]/div[2]/i/text()').extract())).replace('\r\n','')).strip()

        link = (temp['url']).replace('g/','g/jianbie_')

        yield scrapy.Request(url=link,callback=self.next5,meta={'temp':temp})

    def next5(self,response):

        temp = response.meta['temp']

        a = response.xpath('/html/body/div[5]/div[1]/div[2]/i/text()').extract()

        temp['鉴别'] = (((''.join(a)).replace('\r\n\t','')).replace('\r','')).strip()




        yield temp

