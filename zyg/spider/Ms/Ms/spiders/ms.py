# -*- coding: utf-8 -*-
import scrapy


class MsSpider(scrapy.Spider):
    name = 'ms'
    allowed_domains = ['jianke.com']
    start_urls = ['https://jianke.com/']

    def parse(self, response):
        search_url = 'https://www.jianke.com/ask/browse/0-1-1'

        yield scrapy.Request(url=search_url,callback=self.next1)


    def next1(self,response):
        node_list = response.xpath('//*[@id="wrap_a"]/div[3]/div[1]/div[1]/ul/li/a/@href').extract()

        for node in node_list:
            link = 'https://www.jianke.com' + node

            yield scrapy.Request(url=link,callback=self.next2)


    def next2(self,response):

        node_list = response.xpath('//*[@id="wrap_a"]/div[3]/div[1]/div[1]/ul/li/a/@href').extract()

        for node in node_list:
            link = 'https://www.jianke.com' + node

            yield scrapy.Request(url=link,callback=self.next3)

    def next3(self,response):

        node_list = response.xpath('//*[@id="wrap_a"]/div[3]/div[1]/div[1]/ul/li/a/@href').extract()
        for node in node_list:
            link = 'https://www.jianke.com' + node

            yield scrapy.Request(url=link,callback=self.next4)

    def next4(self,response):

        node_list = response.xpath('//*[@id="wrap_a"]/div[3]/div[1]/div[1]/ul/li/a/@href').extract()

        for node in node_list:
            link = 'https://www.jianke.com' + node
            # print(link+'11111111111111111111111')

            yield scrapy.Request(url=link,callback=self.next5)

    def next5(self,response):


        for i in range(1000):

            link = (response.url).replace('-1-1',('-3-'+str(i)))


            yield scrapy.Request(url=link,callback=self.next6)

    def next6(self,response):
        node_list = response.xpath('//*[@id="tabBox1"]/div/div/ul[2]/li/dl/dd/span/a/@href').extract()
        temp = {}
        for node in node_list:
            link = 'https://www.jianke.com' + node


            yield scrapy.Request(url=link,callback=self.next7)

    def next7(self,response):

        temp = {}

        temp['url'] = response.url

        temp['questions'] = response.xpath('//*[@class="why"]/h1/text()').extract_first()

        temp['answer'] = ''.join(response.xpath('//*[@class="an_cont"]/dl/dt//text()').extract())

        yield temp




