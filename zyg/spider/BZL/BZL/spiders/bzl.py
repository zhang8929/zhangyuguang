# -*- coding: utf-8 -*-
import scrapy
import time
import random

class BzlSpider(scrapy.Spider):
    name = 'bzl'
    allowed_domains = ['360bzl.com']
    start_urls = ['http://www.360bzl.com']

    def parse(self, response):

        search_url = "http://www.360bzl.com/ask/fenlei/2/"
        a = random.uniform(1,5)
        time.sleep(a)
        yield scrapy.Request(url=search_url,callback=self.next1)

    def next1(self,response):

        node_list = response.xpath('//*[@class="catetag"]/a/@href').extract()

        for link in node_list:
            a = random.uniform(1,5)
            time.sleep(a)
            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):

        node_list = response.xpath('//*[@class="catetag"]/a/@href').extract()

        for node in node_list:
            for i in range(100):
                link = node +'2/' + str(i) + '/'
                a = random.uniform(1,5)
                time.sleep(a)
                yield scrapy.Request(url=link,callback=self.next3)

    def next3(self,response):
        node_list = response.xpath('//*[@class="question_con"]/ul/li/span/a/@href').extract()

        for node in node_list:
            a = random.uniform(1,5)
            time.sleep(a)
            yield scrapy.Request(url=node,callback=self.next4)

    def next4(self,response):

        node_list =response.xpath('//*[@class="question_con"]/ul/li/a/@href').extract()

        for node in node_list:
            a = random.uniform(1,5)
            time.sleep(a)            
            
            yield scrapy.Request(url=node,callback=self.next5)

    def next5(self,response):

        temp ={}

        temp['questions'] = response.xpath('//*[@class="que_detaila"]/dl/dd/ul/text()').extract_first()

        temp['answers'] = ((''.join(response.xpath('//*[@class="satisfy_main"]/div[1]/div[1]/div[1]/dl/dd//text()').extract())).replace(' ','')).strip()


        temp['des'] = (((''.join(response.xpath('//*[@class="que_detailb1"]/dl[3]//text()').extract())).replace(' ','')).replace('\r\n','')).strip()

        temp['url'] = response.url

        yield temp



