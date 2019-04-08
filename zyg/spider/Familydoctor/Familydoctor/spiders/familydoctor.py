# -*- coding: utf-8 -*-
import scrapy


class FamilydoctorSpider(scrapy.Spider):
    name = 'familydoctor'
    allowed_domains = ['ask.familydoctor.com.cn']
    start_urls = ['http://ask.familydoctor.com.cn/']

    def parse(self, response):
        search_url = 'http://ask.familydoctor.com.cn/jbk/'

        for i in range(99):

            for a in range(10):

                link = search_url + str(i)+ '?page=' + str(a) +'&'

                yield scrapy.Request(url=link,callback=self.next)


    def next(self,response):

        node_list = response.xpath('/html/body/div/div/div/div/div/a/@href').extract()

        for node in node_list:
            # print(node)
            for i in range(1000):
                link = node + '?page='+str(i)+'&'

                yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        print(response.url)
        node_list = response.xpath('//*[@class="cont faq-list"]/dl/dt/p/a/@href').extract()
        #print(node_list)
        try:
            for link in node_list:
                print(link)

                yield scrapy.Request(url=link,callback=self.next2)
        except:
            pass

    def next2(self,response):
        print('*'*1000,response.url)
        temp = {}

        temp['question'] = ((''.join(response.xpath('//*[@class="main-sec quest-info"]/div/div[2]/p/text()').extract())).replace('\r\n','')).strip()

        temp['answer'] = ((response.xpath('//*[@class="answer-info-cont"]/dd/p/text()').extract_first()).replace('\r\n','')).strip()

        temp['sick_name'] = response.xpath('//*[@class="main-sec quest-info"]/div[1]/p[1]/a/text()').extract_first()



        yield temp
