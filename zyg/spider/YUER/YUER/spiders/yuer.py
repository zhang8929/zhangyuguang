# -*- coding: utf-8 -*-
import scrapy


class YuerSpider(scrapy.Spider):
    name = 'yuer'
    allowed_domains = ['ask.ci123.com']
    start_urls = ['http://ask.ci123.com/']

    def parse(self, response):
        search_url = 'http://ask.ci123.com/categories/listquestion/solved?p='
        for i in range(37153):
            link = search_url + str(i)

            yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('//*[@class="list_u_down"]/li/div/a/@href').extract()

        for node in node_list:
            link = 'http://ask.ci123.com' + node

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['questions'] = response.xpath('//*[@id="ask_middle2"]/div[5]/div[1]/ul[2]/table//tr[1]/td[2]/h3/text()').extract_first()

        temp['des'] = response.xpath('//*[@id="ask_middle2"]/div[5]/div[1]/ul[2]/table//tr[1]/td[2]/span/text()').extract_first()

        temp['answer'] = response.xpath('//*[@id="ask_middle2"]/div[5]/div[3]/div/ul[2]/table//tr[1]/td[2]/span/text()').extract_first()

        temp['url'] = response.url





        yield temp
