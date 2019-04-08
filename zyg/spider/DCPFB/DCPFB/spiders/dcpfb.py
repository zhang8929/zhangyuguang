# -*- coding: utf-8 -*-
import scrapy


class DcpfbSpider(scrapy.Spider):
    name = 'dcpfb'
    allowed_domains = ['dcpfb.com']
    start_urls = ['http://www.dcpfb.com/']

    def parse(self, response):
        search_url = 'http://www.dcpfb.com/ask/browser-lm-3-'

        for i in range(4884):
            link = search_url + str(i) + '.html'
            yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('//*[@class="know_box"]/div/ul/li/div/a/@href').extract()

        for node in node_list:
            yield scrapy.Request(url=node,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['url'] = response.url

        temp['questions'] = (response.xpath('//*[@class="wdbknr"]/h2/text()').extract_first()).replace('咨询标题：','')

        temp['answer'] = (((''.join(response.xpath('//*[@class="best_answer_show"]//text()').extract())).replace('\r\n','')).replace(' ','')).strip()

        temp['des'] = response.xpath('//*[@class="wdms"]/div[3]/p[1]/text()').extract_first()


        yield temp

