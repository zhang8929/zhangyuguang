# -*- coding: utf-8 -*-
import scrapy


class Ask9939Spider(scrapy.Spider):
    name = 'ask9939'
    allowed_domains = ['ask.9939.com']
    start_urls = ['http://ask.9939.com/']

    def parse(self, response):
        search_url = 'http://ask.9939.com/wenti/'
        for i in range(50):
            link = search_url + str(i) + '.html'

            yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):

        node_list = response.xpath('//*[@class="mapsdata"]/li/a/@href').extract()


        for node in node_list:
            for i in range(100):
                a = str(i)+'.html'
                link = node.replace('1.html',a)

                yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        # print(response.url)

        node_list = response.xpath('//*[@class="period"]/li/div/h3/a/@href').extract()

        for node in node_list:
            print(node)
            yield scrapy.Request(url=node, callback=self.next3)

    def next3(self,response):
        print('1111111111111111111111111111111111111111111')

        temp = {}

        temp['url'] = response.url

        temp['questions'] = response.xpath('//*[@class="user_ask"]/div[2]/p/text()').extract_first()

        temp['answer'] = ((''.join(response.xpath('//*[@class="descip paint1"]/p/text()').extract())).replace('\r\n','')).strip()

        yield temp