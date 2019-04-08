# -*- coding: utf-8 -*-
import scrapy


class EwsosSpider(scrapy.Spider):
    name = 'ewsos'
    allowed_domains = ['ask.ewsos.com']
    start_urls = ['https://ask.ewsos.com/']

    def parse(self, response):
        search_url = 'https://ask.ewsos.com/browse/0-4-'
        for i in range(2859):
            link = search_url + str(i) + '.html'
            yield scrapy.Request(url=link,callback=self.next1)
    def next1(self,response):
        node_list = response.xpath('//*[@class="qatxt"]/div/span/a/@href').extract()
        for node in node_list:
            if '-'not in node:
                link = 'https://ask.ewsos.com' + node
                yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):

        temp = {}

        temp['url'] = response.url

        temp['questions'] = ((''.join(response.xpath('//*[@class="wtbox"]/h1/strong/text()').extract())).replace('\r\n','')).strip()

        temp['answer'] = (((((''.join(response.xpath('//*[@class="mone"]/p[1]/text()').extract())).replace('\r\n','')).strip()).replace('\r','')).replace(' ','')).strip()

        temp['dev'] = (((''.join(response.xpath('//*[@class="wny"]/p[2]/text()').extract())).replace('\r\n','')).strip()).replace(' ','')

        yield temp


