# -*- coding: utf-8 -*-
import scrapy


class YlaqSpider(scrapy.Spider):
    name = 'ylaq'
    allowed_domains = ['youlai.cn']
    start_urls = ['https://www.youlai.cn/']

    def parse(self, response):

        for i in range(2295):
            for a in range(100):
                link = 'https://www.youlai.cn/dise/asklist/' + str(i)+ '_'+ str(a) + '.html'
                # print(link)
                yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        temp = {}
        temp['sick_name'] = response.xpath('/html/body/div/div/p/text()').extract_first()
        try:

            node_list = response.xpath('/html/body/div[3]/div[1]/ul/li/h3/a/@href').extract()

            for node in node_list:
                node1 = 'https://www.youlai.cn' + node
                yield scrapy.Request(url=node1,callback=self.next2,meta={'temp':temp})





            # print(response.url)

        except:
            pass

    def next2(self, response):

        temp = response.meta['temp']

        a = response.xpath('/html/body/div[2]/div[1]/dl/dd/p/text()').extract_first()

        q = response.xpath('/html/body/div[2]/div[1]/div/div[2]/p/text()').extract_first()

        temp[a] = q

        yield temp
