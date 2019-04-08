# -*- coding: utf-8 -*-
import scrapy


class SanjiuSpider(scrapy.Spider):
    name = 'Sanjiu'
    allowed_domains = ['jbk.39.net']
    start_urls = ['http://jbk.39.net/bw/']

    def parse(self, response):   #进到疾病主页面

        nodes = response.xpath('//*[@class="lookup_department lookup_cur"]/div[1]/ul/li/a/@href').extract()
        for node in nodes:
            node = 'http://jbk.39.net' + node
            # print(node)
            yield scrapy.Request(url=node,callback=self.next1)

    def next1(self, response):#进了妇科页面---去点下面分科室
        nodes1 = response.xpath('//*[@class="lookup_second_box first_line"]/ul/li/a/@href').extract()
        nodes2 = response.xpath('//*[@class="lookup_second_box second_line"]/ul/li/a/@href').extract()

        list1=[]
        for node in nodes1:
            node = 'http://jbk.39.net' + node
            list1.append(node)

        for node in nodes2:
            node = 'http://jbk.39.net' + node
            list1.append(node)


        for node in list1:
            # print(node)
            yield scrapy.Request(url=node,callback=self.next2)

    def next2(self,response):#点到分科室
        for i in range(1,201):
            node = response.url[:-1]+'_t1_p%s/'%i
            # print(node)
            yield scrapy.Request(url=node,callback=self.next3)

    def next3(self,response):#进详情页
        # print(response.url)
        nodes = response.xpath('//*[@class="result_item_top"]/p[1]/a/@href').extract()

        for node in nodes:
            yield scrapy.Request(url=node,callback=self.next4)

    def next4(self,response):
        tmp_dict = {}
        tmp_dict['名称'] = response.xpath('//*[@class="disease"]/h1/text()').extract()
        tmp_dict['别名'] = response.xpath('//*[@class="information_ul"]/li[1]/span/text()').extract()
        # print(tmp_dict)
        node = response.xpath('//*[@class="information_box"]/p/a/@href').extract()[0]
        # print(node)

        yield  scrapy.Request(url=node,callback=self.next5,meta={'tmp':tmp_dict})

    def next5(self,response):
        # print(response.url)
        tmp_dict = response.meta['tmp']
        # print('===')
        # print(tmp_dict)
        tmp_dict['基本信息'] = response.xpath('//*[@class="introduction"]/text()').extract()

        # print(tmp_dict['基本信息'])
        tmp_dict['并发疾病'] = response.xpath('//*[@class="disease_box"][2]/ul/li[6]/span[2]/a/text()').extract()

        # print(tmp_dict)
        yield tmp_dict












