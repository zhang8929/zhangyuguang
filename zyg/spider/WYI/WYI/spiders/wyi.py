# -*- coding: utf-8 -*-
import re

import scrapy


class WyiSpider(scrapy.Spider):
    name = 'wyi'
    allowed_domains = ['wenyw.com']
    start_urls = ['https://wenyw.com/']

    def parse(self, response):
        node_list = response.xpath('//*[@class="mainnavwrap"]/div/a/@href').extract()
        # print(node_list)

        for node in node_list:
            if node[-1] != 'l':
                pass
            else:
                yield scrapy.Request(url=node,callback=self.next1)

    def next1(self,response):

        for i in range(201):
            link = (response.url).replace('.html',('/2/'+str(i)+'.html'))

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        node_list = response.xpath('//*[@class="iask10_con"]/ul/li/span/a/@href').extract()

        for node in node_list:
            yield scrapy.Request(url=node,callback=self.next3)

    def next3(self,response):


        node_list = response.xpath('//*[@class="iask10"]/div/ul/li/a/@href').extract()

        for node in node_list:
            yield scrapy.Request(url=node,callback=self.next4)

    def next4(self,response):
        print(response.url)

        temp = {}

        temp['url'] = response.url

        temp['questions'] = response.xpath('//*[@class="iask_detail01a"]/dl/dd/ul/h1/text()').extract_first()

        temp['des'] = (''.join(response.xpath('//*[@class="iask_detail01b1"]/dl/dd/text()').extract())).replace('\r\n','')

        temp['answer'] = (''.join(response.xpath('//*[@class="iask_answer02a"]/dl[1]/dd[1]/text()').extract())).replace('\r\n','')



        yield temp
