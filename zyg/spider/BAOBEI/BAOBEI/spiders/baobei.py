# -*- coding: utf-8 -*-
import scrapy


class BaobeiSpider(scrapy.Spider):
    name = 'baobei'
    allowed_domains = ['wenda.qbaobei.com']
    start_urls = ['http://wenda.qbaobei.com/']

    def parse(self, response):
        search_url = 'http://wenda.qbaobei.com/category/view/all/2/'

        for i in range(21235):
            link = search_url + str(i) + '.html'

            yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li/span[3]/a[1]/@href').extract()
        print(node_list)
        for node in node_list:
            link = 'http:' + node

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['url'] = response.url

        temp['questions'] = response.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/h1/text()').extract_first()

        temp['answer'] = response.xpath('//*[@class="qa-content"]/p/text()').extract_first()



        temp['auther'] = response.xpath('//*[@id="gift_box"]/div/div[2]/div/span[1]/text()').extract_first()



        yield temp

