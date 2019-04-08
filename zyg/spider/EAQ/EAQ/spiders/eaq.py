# -*- coding: utf-8 -*-
import scrapy


class EaqSpider(scrapy.Spider):
    name = 'eaq'
    allowed_domains = ['ask.qqyy.com']
    start_urls = ['http://ask.qqyy.com/']

    def parse(self, response):
        list1 = ['http://ask.qqyy.com/jb_398/','http://ask.qqyy.com/jb_582/','http://ask.qqyy.com/jb_1039/','http://ask.qqyy.com/jb_1076/','http://ask.qqyy.com/jb_1351/','http://ask.qqyy.com/jb_1387/','http://ask.qqyy.com/jb_1518/','http://ask.qqyy.com/jb_1521/','http://ask.qqyy.com/jb_1606/','http://ask.qqyy.com/jb_1837/','http://ask.qqyy.com/jb_2089/','http://ask.qqyy.com/jb_2429/','http://ask.qqyy.com/jb_9474/','http://ask.qqyy.com/jb_3071/','http://ask.qqyy.com/jb_3631/','http://ask.qqyy.com/jb_3727/','http://ask.qqyy.com/jb_3731/','http://ask.qqyy.com/jb_3745/','http://ask.qqyy.com/jb_3847/','http://ask.qqyy.com/jb_4138/','http://ask.qqyy.com/jb_4294/','http://ask.qqyy.com/jb_4608/','http://ask.qqyy.com/jb_4758/','http://ask.qqyy.com/jb_9473/','http://ask.qqyy.com/jb_4896/','http://ask.qqyy.com/jb_5170/','http://ask.qqyy.com/jb_5504/','http://ask.qqyy.com/jb_5519/','http://ask.qqyy.com/jb_5655/','http://ask.qqyy.com/jb_5774/','http://ask.qqyy.com/jb_6004/','http://ask.qqyy.com/jb_6194/','http://ask.qqyy.com/jb_9472/','http://ask.qqyy.com/jb_9471/','http://ask.qqyy.com/jb_6501/','http://ask.qqyy.com/jb_6702/','http://ask.qqyy.com/jb_7353/','http://ask.qqyy.com/jb_7534/']
        for a in list1:
            search_url = a + '1_'
            for i in range(10000):
                link = search_url + str(i) + '.html'
                # print(link)
                yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        node_list = response.xpath('/html/body/div[4]/div[1]/div[4]/ul/li/a/@href').extract()

        for node in node_list:
            link = 'http://ask.qqyy.com' + node

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        # print(response.url)

        temp = {}



        # a = response.xpath('//*[@class="ask_box"]/p/text()').extract_first()
        #
        # temp['question'] = (a).strip()
        #
        # b  = response.xpath('//*[@class="adiv_int"]/p[1]/text()').extract_first()
        #
        #
        # temp['answer'] = (''.join(b)).replace('\n','').strip()

        temp['url'] = response.url



        yield temp
        #
        # except Exception as f:
        #     print(f)

