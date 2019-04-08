# -*- coding: utf-8 -*-
import scrapy


class JiankeSpider(scrapy.Spider):
    name = 'jianke'
    allowed_domains = ['jianke.com']
    start_urls = ['https://www.jianke.com/']

    def parse(self, response):
        lis1 = ['https://www.jianke.com/ask/Browse/25-3-', 'https://www.jianke.com/ask/Browse/01-3-',
                'https://www.jianke.com/ask/Browse/03-3-', 'https://www.jianke.com/ask/Browse/501-3-',
                'https://www.jianke.com/ask/Browse/2-3-', 'https://www.jianke.com/ask/Browse/4-3-',
                'https://www.jianke.com/ask/Browse/601-3-', 'https://www.jianke.com/ask/Browse/7-3-',
                'https://www.jianke.com/ask/Browse/9-3-', 'https://www.jianke.com/ask/Browse/10-3-',
                'https://www.jianke.com/ask/Browse/11-3-', 'https://www.jianke.com/ask/Browse/12-3-',
                'https://www.jianke.com/ask/Browse/13-3-','https://www.jianke.com/ask/Browse/305-3-']
        for search_url in lis1:

            for i in range(29437):
                link = search_url + str(i)

                yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('//*[@id="tabBox1"]/div/div/ul[2]/li/dl/dd/span/a/@href').extract()

        for node in node_list:
            link = 'https://www.jianke.com' + node
            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['url'] = response.url


        temp['answer'] = ((''.join(response.xpath('//*[@class="an_cont"]/dl/dt//text()').extract())).replace('\r\n','')).replace(' ','')


        temp['question'] = response.xpath('//*[@class="why"]/h1/text()').extract_first()

        temp['des'] = response.xpath('//*[@class="pd_txt"]/text()').extract_first()


        yield temp
