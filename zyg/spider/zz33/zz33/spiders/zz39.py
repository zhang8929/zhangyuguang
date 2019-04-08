# -*- coding: utf-8 -*-
import scrapy


class Zz39Spider(scrapy.Spider):
    name = 'zz39'
    allowed_domains = ['jbk.39.net']
    start_urls = ['http://jbk.39.net/']

    def parse(self, response):
        search_url = 'http://jbk.39.net/bw_t2_p'

        for i in range(201):
            link = search_url + str(i)

            yield scrapy.Request(url=link, callback=self.detail)

    def detail(self,response):

        node_list = response.xpath('//*[@id="res_subtab_1"]/div/dl/dt/h3/a/@href').extract()

        for node in node_list:
            yield scrapy.Request(url=node,callback=self.next1)

    def next1(self,response):
        temp = {}

        temp['症状名称'] = response.xpath('/html/body/section[1]/header/div[1]/a/h1/text()').extract_first()

        temp['image_url'] = response.xpath('/html/body/section[1]/div[2]/article/div[1]/div[1]/a/img/@src').extract_first()

        temp['简介'] = response.xpath('//*[@id="intro"]/p/text()').extract_first()
        temp['url'] = response.url


        print(temp)
