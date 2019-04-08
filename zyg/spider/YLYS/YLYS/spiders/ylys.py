# -*- coding: utf-8 -*-
import scrapy

with open('./url.json','r')as f:
    content = f.read().splitlines()
class YlysSpider(scrapy.Spider):
    name = 'ylys'
    allowed_domains = ['youlai.cn']
    start_urls = ['https://www.youlai.cn/']

    def parse(self, response):

        for node in content:
            node1 = 'https://www.youlai.cn' + node
            yield scrapy.Request(url=node1,callback=self.next1)

    def next1(self,response):
        temp = {}

        temp['sick_name'] = response.xpath('/html/body/div[2]/div/p/text()').extract_first()

        temp['url'] = response.url

        temp['挂号科室'] = response.xpath('/html/body/div[3]/div[1]/dl/dt/p[1]/span/a/text()').extract()

        temp['相关症状'] = response.xpath('/html/body/div[3]/div[1]/dl/dd[1]/p[1]/span/text()').extract_first()

        temp['发病部位'] = response.xpath('/html/body/div[3]/div[1]/dl/dt/p[2]/span/text()').extract()

        temp['相关疾病'] = response.xpath('/html/body/div[3]/div[1]/dl/dd[1]/p[2]/span/a/text()').extract()

        temp['多发人群'] = response.xpath('/html/body/div[3]/div[1]/dl/dt/p[3]/span/text()').extract_first()

        temp['相关检查'] = response.xpath('/html/body/div[3]/div[1]/dl/dd[1]/p[3]/span/text()').extract_first()

        temp['治疗方法'] = response.xpath('/html/body/div[3]/div[1]/dl/dt/p[4]/span/text()').extract_first()

        temp['相关手术'] = response.xpath('/html/body/div[3]/div[1]/dl/dd[1]/p[4]/span/text()').extract()

        temp['是否传染'] = response.xpath('/html/body/div[3]/div[1]/dl/dt/p[5]/span/text()').extract_first()

        temp['相关药品'] = response.xpath('/html/body/div[3]/div[1]/dl/dd[1]/p[5]/span/text()').extract()

        temp['是否遗传'] = response.xpath('/html/body/div[3]/div[1]/dl/dt/p[6]/span/text()').extract_first()

        temp['治疗费用'] = response.xpath('/html/body/div[3]/div[1]/dl/dd[1]/p[6]/span/text()').extract_first()

    #     link = 'https://www.youlai.cn' + response.xpath('/html/body/div[2]/div/ul/li[4]/a/@href').extract_first()
    #
    #     yield scrapy.Request(url=link,callback=self.next2,meta={'temp':temp})
    # def next2(self,response):
    #     temp = response.meta['temp']
    #
    #     temp['url'] = response.url
    #
    #     node_list = response.xpath('/html/body/div[3]/div[1]/ul/li/h3/a/@href').extract()
    #     for node in node_list:
    #         yield
    #
    #     print(response.text)

        yield temp
