# -*- coding: utf-8 -*-
import scrapy


class YaofangwangSpider(scrapy.Spider):
    name = 'yaofangwang'
    allowed_domains = ['yaofangwang.com']
    start_urls = ['https://www.yaofangwang.com/']

    def parse(self, response):
        search_url = 'https://www.yaofangwang.com/ask/'
        yield scrapy.Request(url=search_url,callback=self.next1)
    def next1(self,response):
        node_list = response.xpath('//*[@id="aspnetForm"]/div/div/div/ul/li/div/a/@href').extract()
        for node in node_list:
            link = 'https://www.yaofangwang.com' + node + 's2/' + 'p'

            for i in range(100):
                link1 = link  + str(i)

                yield scrapy.Request(url=link1,callback=self.next2)

    def next2(self,response):
        node_list = response.xpath('//*[@id="aspnetForm"]/div[4]/div/div/div/div/ul/li/div/a/@href').extract()
        for node in node_list:
            link = 'https:' + node
            yield scrapy.Request(url=link,callback=self.next3)

    def next3(self,response):
        temp = {}
        temp['questions'] = response.xpath('//*[@id="aspnetForm"]/div[4]/div[1]/div/div[1]/span/text()').extract_first()

        temp['answer'] = ((response.xpath('//*[@class="ask-item"]/div[2]/p/text()').extract_first()).replace('\r\n','')).strip()




        temp['url'] = response.url

        yield temp