# -*- coding: utf-8 -*-
import scrapy


class ClubaqSpider(scrapy.Spider):
    name = 'clubaq'
    allowed_domains = ['club.xywy.com']
    start_urls = ['http://club.xywy.com/']

    def parse(self, response):
        search_url = 'http://club.xywy.com/kswd_list.htm'

        yield scrapy.Request(url=search_url,callback=self.next1)

    def next1(self,response):

        link_list = response.xpath('//*[@class="c-part-hd"]/ul/li/a/@href').extract()

        for node in link_list:
            link = 'http://club.xywy.com' + (node.replace('.htm','_answer.htm')).replace('big','list')

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        # print(response.url)

        list1 = response.xpath('//*[@class="ks_287"]/ul/li/a/@href').extract()

        # print(len(list1))
        list2 = response.xpath('//*[@class="c-part-con pr clearfix"]/ul/li/a/@href').extract()

        # print(list2)

        list1.extend(list2)
        # print(len(list1))


        for node in list1:

            for i in range(201):
                a = '_answer_'+str(i)+'.htm'

                link = 'http://club.xywy.com' + (node.replace('.htm',a)).replace('small','list')
                # print(link)

                yield scrapy.Request(url=link,callback=self.next3)

    def next3(self,response):
        # temp = {}


        # print(response.url)
        # pass
        node_list = response.xpath('//*[@class="f12 kstable"]//tr/td/a[2]/@href').extract()

        for link in node_list:
            yield scrapy.Request(url=link,callback=self.next4)

    def next4(self,response):
        temp = {}
        temp['url'] = response.url

        temp['question'] = ((response.xpath('//*[@class="clearfix pl29 mr30"]/div/text()').extract_first()).replace('\r\n','')).replace('\t','')

        temp['answer'] = (''.join(response.xpath('//*[@class="pt10 mb5 clearfix pr qsdetail"]/div[2]/div[1]//text()').extract())).strip()

        yield temp