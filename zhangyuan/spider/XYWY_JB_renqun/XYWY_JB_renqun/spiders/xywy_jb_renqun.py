# -*- coding: utf-8 -*-
import scrapy


class XywyJbRenqunSpider(scrapy.Spider):
    name = 'xywy_jb_renqun'
    allowed_domains = ['jib.xywy.com']
    start_urls = ['http://jib.xywy.com/']

    def parse(self, response):
        lists = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s','t','u','v','w','x','y','z']
        for zi in lists:
            node = 'http://jib.xywy.com/html/'+zi+'.html'
            yield scrapy.Request(url=node,callback=self.next1)

    def next1(self,response):
        # print(response.url)
        nodes = response.xpath('//*[@class="fl jblist-con-ear"]/div/ul/li/a/@href').extract()
        for node in nodes:
            node = 'http://jib.xywy.com'+node
            # print(node)
            yield scrapy.Request(url=node,callback=self.next2)

    def next2(self,response):
        # print(response.url)
        tmp = {}
        tmp['名称'] = response.xpath('//*[@class="jb-name fYaHei gre"]/text()').extract()[0]
        tmp['多发人群'] = response.xpath('//*[@class="fl jib-common-sense"]/p[1]/span[2]/text()').extract()[0]

        link = 'http://jib.xywy.com'+response.xpath('//*[@class="jib-navbar-side pr"][2]/ul/li[1]/a/@href').extract()[0]

        yield scrapy.Request(url=link,callback=self.next3,meta={'tmp':tmp})

    def next3(self,response):
        tmp = response.meta['tmp']
        tmp['病症详述'] = ''.join(response.xpath('//*[@class="jib-articl fr f14 jib-lh-articl"]/p//text()').extract())

        yield tmp

