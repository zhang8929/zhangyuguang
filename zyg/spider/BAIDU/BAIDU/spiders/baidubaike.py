# -*- coding: utf-8 -*-
import scrapy
with open('./zyy75956.json','r')as f:
    content = f.read().splitlines()

class BaidubaikeSpider(scrapy.Spider):
    name = 'baidubaike'
    allowed_domains = ['baidu.com']
    start_urls = ['https://baidu.com/']

    def parse(self, response):
        search_url = 'http://baike.baidu.com/science/medical'
        yield scrapy.Request(url=search_url,callback=self.next1)

    def next1(self,response):
        # print (response.url)
        for link in content:
            # print(link)

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['url'] = response.url

        temp['entry'] = response.xpath('//*[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract_first()

        temp['content'] = ((''.join(response.xpath('//*[@class="main-content"]//text()').extract())).replace('\r\n','')).replace('\n','')






        yield temp



