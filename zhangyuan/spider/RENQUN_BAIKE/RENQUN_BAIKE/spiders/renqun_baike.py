# -*- coding: utf-8 -*-
import scrapy


class RenqunBaikeSpider(scrapy.Spider):
    name = 'renqun_baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/']

    def parse(self, response):
        with open('/home/python/Desktop/baike.txt','r',encoding='utf-8') as file:
            contents = file.readlines()
            print('===')
            print(type(contents))
            for name in contents:
                node = 'https://baike.baidu.com/item/'+name[:-1]
                yield scrapy.Request(url=node,callback=self.next1)

    def next1(self,response):
        tmp = {}
        tmp['名称']=response.xpath('//*[@class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"]/dd/h1/text()').extract()[0]
        # tmp[response.xpath('//*[@class="basic-info cmn-clearfix"]/dl[1]/dt[1]/text()')]=response.xpath('//*[@class="basic-info cmn-clearfix"]/dl[1]/dd[1]/text()')
        # tmp[response.xpath('//*[@class="basic-info cmn-clearfix"]/dl[1]/dt[1]/text()')]=response.xpath('//*[@class="basic-info cmn-clearfix"]/dl[1]/dd[1]/text()')
        keys = response.xpath('//*[@class="basic-info cmn-clearfix"]/dl/dt/text()').extract()
        values = response.xpath('//*[@class="basic-info cmn-clearfix"]/dl/dd/text()').extract()
        for i in range(0,len(keys)-1):
            tmp[keys[i]] = values[i]
            i += 1

        yield tmp

