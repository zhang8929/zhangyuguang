# -*- coding: utf-8 -*-
import scrapy


class KzjSpider(scrapy.Spider):
    name = 'kzj'
    allowed_domains = ['kzj365.com']
    start_urls = ['http://www.kzj365.com/']

    def parse(self, response):
        search_url = 'http://www.kzj365.com/ask/'
        yield scrapy.Request(url=search_url,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('//*[@class="wdfl"]/dd/ul/li/div/a/@href').extract()
        print(node_list)
        for node in node_list:
            link = 'http://www.kzj365.com' + node
            for i in range(100):
                link1 = link.replace('.html','-4-'+str(i)+'.html')
                yield scrapy.Request(url=link1,callback=self.next2)

    def next2(self,response):

        node_list = response.xpath('//*[@class="tbl_type"]/span/a[2]/@href').extract()

        for node in node_list:
            link = 'http://www.kzj365.com' + node

            yield scrapy.Request(url=link,callback=self.next3)

    def next3(self,response):

        temp = {}

        temp['url'] = response.url

        temp['questions'] = (response.xpath('//*[@class="clearfix"]/dd/h1/text()').extract_first()).replace('\n','')

        temp['answers'] = (response.xpath('//*[@class="yd"]/dl/dd/div/text()').extract_first()).replace('\n','')

        yield temp
