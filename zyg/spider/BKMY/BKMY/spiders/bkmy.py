# -*- coding: utf-8 -*-
import scrapy


class BkmySpider(scrapy.Spider):
    name = 'bkmy'
    allowed_domains = ['baikemy.com']
    start_urls = ['http://www.baikemy.com/']

    def parse(self, response):

        search_url = 'https://www.baikemy.com/ask/asksquare'

        yield scrapy.Request(url=search_url,callback=self.next1)

    def next1(self,response):
        node_list =response.xpath('//*[@id="tab_curr"]/li/a/@href').extract()
        for node in node_list:
            link = 'https://www.baikemy.com' + node
            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        node_list =response.xpath('//*[@id="zx_content"]/div/div/ul/li/div/a/@href').extract()
        for node in node_list:
            link = 'https://www.baikemy.com' + node + '?pageIndex='
            for i in range(10):
                link1 = link + str(i)
                yield scrapy.Request(url=link1,callback=self.next3)

    def next3(self,response):
        node_list = response.xpath('//*[@id="zx_content"]/div[3]/div/table//tr/td/span/a/@href').extract()

        for node in node_list:
            yield scrapy.Request(url=node,callback=self.next4)

    def next4(self,response):

        temp = {}

        temp['questions'] = ''.join(response.xpath('/html/body/div/div/div/div[1]/div[1]/text()').extract())

        temp['des'] = ''.join(response.xpath('/html/body/div[6]/div/div/div/div[4]/text()').extract())

        temp['answer'] = ''.join(response.xpath('/html/body/div[6]/div/div/div/div[6]/div[2]/text()').extract())

        temp['url'] = response.url

        yield temp