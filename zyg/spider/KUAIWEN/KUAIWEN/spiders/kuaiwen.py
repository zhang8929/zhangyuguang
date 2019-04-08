# -*- coding: utf-8 -*-
import scrapy


class KuaiwenSpider(scrapy.Spider):
    name = 'kuaiwen'
    allowed_domains = ['kuaiwen.pcbaby.com.cn']
    start_urls = ['https://kuaiwen.pcbaby.com.cn/']

    def parse(self, response):
        search_url = 'https://kuaiwen.pcbaby.com.cn/hot/h26936/p'
        for i in range(237):
            link = search_url + str(i) + '.html'
            yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('//*[@class="lBox-tb"]/ul/li/div/a/@href').extract()
        for node in node_list:
            link = 'https:' + node

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['url'] = response.url

        temp['questions'] = response.xpath('//*[@class="wt-box mb30 part"]/dl/dd/p[2]/text()').extract_first()

        temp['answer'] = ''.join(response.xpath('//*[@class="wt-wd wt-bestAns"]/dl/dd/div/text()').extract())


        yield temp







        pass
