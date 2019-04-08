# -*- coding: utf-8 -*-
import scrapy


class XywyZzSpider(scrapy.Spider):
    name = 'xywy_zz'
    allowed_domains = ['zzk.xywy.com']
    start_urls = ['http://zzk.xywy.com/p/a.html']

    def parse(self, response):
        # print(response.url)
        nodes = response.xpath('//*[@class="fr jblist-con-zm fYaHei"]/ul/li/a/@href').extract()
        for node in nodes:
            next_link = 'http://zzk.xywy.com'+node
            yield scrapy.Request(url=next_link,callback=self.next1)

    def next1(self,response):
        # print(response.url)
        nodes = response.xpath('//*[@id="illA"]/div//li/a/@href').extract()
        for node in nodes:
            next_link = 'http://zzk.xywy.com'+node
            yield scrapy.Request(url=next_link,callback=self.next2)

    def next2(self,response):
        # print(response.url)
        next_link = response.url.replace('gaishu','jieshao')
        yield scrapy.Request(url=next_link,callback=self.next3)

    def next3(self,response):
        # print(response.url)
        dict = {}
        dict['名称'] = response.xpath('//*[@class="jb-name fYaHei gre"]/text()').extract_first()
        dict['定义'] = ''.join(response.xpath('//*[@class="wrap mt10 clearfix graydeep"]/div[1]/div[1]/div[2]/p//text()').extract())

        yield dict




