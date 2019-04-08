# -*- coding: utf-8 -*-
import scrapy


class Ask120Spider(scrapy.Spider):
    name = 'ask120'
    allowed_domains = ['120ask.com']
    start_urls = ['http://120ask.com/']

    def parse(self, response):
        search_url = 'http://www.120ask.com/list/over/'

        yield scrapy.Request(url=search_url,callback=self.next1)


    def next1(self,response):

        node_list= response.xpath('//*[@id="list"]/div[1]/ul/li/a/@href').extract()
        # print(node_list)
        for node in node_list:
            node = 'http:' + node
            yield scrapy.Request(url=node,callback=self.next2)

    def next2(self,response):

        node_list = response.xpath('//*[@id="list"]/div[1]/ul/li/a/@href').extract()
        # print(node_list)
        for node in node_list:
            link = 'http:' + node

            yield scrapy.Request(url=link,callback=self.next3)

    def next3(self,response):


        pass

