# -*- coding: utf-8 -*-
import scrapy

with open('/home/python/Desktop/zz.json','r')as f:
    content = f.read().splitlines()
    # a = 'https://jibing.51240.com/,%E5%8F%91%E7%83%AD,__jibing/'
    print(len(content))
class ZzSpider(scrapy.Spider):
    name = 'zz'
    allowed_domains = ['jibing.51240.com']
    start_urls = ['https://jibing.51240.com/']

    def parse(self, response):
        print(response.text)
        temp = {}

        for i in content:
            # temp['category'] = i

            link = response.url + ',' + i + ',__jibing/'

            yield scrapy.Request(url=link,callback=self.next1,meta={'temp':temp})


    def next1(self,response):
        temp = response.meta['temp']

        node_list = response.xpath('//*[@id="main_content"]/ul/li/a/@href').extract()

        for node in node_list:

            link = 'https://jibing.51240.com' + node

            yield scrapy.Request(url=link,callback=self.next2,meta={'temp':temp})

    def next2(self,response):

        temp = response.meta['temp']

        temp['sick_name'] = response.xpath('//*[@id="main_content"]/h2/text()').extract_first()

        a = response.xpath('//*[@id="main_content"]/table[1]//tr/td/table//tr[1]/td[1]/text()').extract_first()

        temp[a] = response.xpath('//*[@id="main_content"]/table[1]//tr/td/table//tr[1]/td[2]/text()').extract()


        b = response.xpath('//*[@id="main_content"]/table[1]//tr/td/table//tr[2]/td[1]/text()').extract_first()

        temp[b] = response.xpath('//*[@id="main_content"]/table[1]//tr/td/table//tr[2]/td[2]/text()').extract_first()

        c = response.xpath('//*[@id="main_content"]/table[1]//tr/td/table//tr[3]/td[1]/text()').extract_first()


        temp[c] = response.xpath('//*[@id="main_content"]/table[1]//tr/td/table//tr[3]/td[2]/text()').extract_first()

        d = response.xpath('//*[@id="main_content"]/table[2]//tr/td/table//tr[1]/td/text()').extract_first()

        temp[d] = response.xpath('//*[@id="main_content"]/table[2]//tr/td/table//tr[2]/td/p/text()').extract_first()

        temp['url'] = response.url

        yield temp




