# -*- coding: utf-8 -*-
import scrapy
import time


class Jbk39Spider(scrapy.Spider):
    name = 'jbk39'
    allowed_domains = ['jbk.39.net']
    start_urls = ['http://jbk.39.net/']

    def parse(self, response):
        print(response.url)
        search_url = 'http://jbk.39.net/bw_t1_p'

        for i in range(201):
            link = search_url + str(i)

            yield scrapy.Request(url=link,callback=self.detail)

    def detail(self,response):
        node_list= response.xpath('//*[@id="res_tab_2"]/div/dl/dt/h3/a/@href').extract()

        # print(node_list)
        # node_list = response.xpath('//*[@id="map"]/div/dl/dd/div[1]/ul/li/span[2]/a/@href').extract()
        #
        list1 = ['http://jbk.39.net/ngs/','http://jbk.39.net/nxs/','http://jbk.39.net/nzf/','http://jbk.39.net/ttty/','http://jbk.39.net/pt/','http://jbk.39.net/xnws/','http://jbk.39.net/nqx/','http://jbk.39.net/nxgjl/']

        for node in node_list:
            if node not in list1:
                time.sleep(0.05)

                yield scrapy.Request(url=node,callback=self.next1)


        # print(node_list)

    def next1(self,response):
        if 'zhengzhuang' not in response.url:
            temp = {}

            temp['url'] = response.url

            #疾病名称
            temp['sick_name'] =  response.xpath('/html/body/section[1]/div[1]/span/b/text()').extract_first()

            list1 = ['典型症状：','治疗方法：','并发症：']
            # 疾病介绍
            # sick_introduce = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[1]/div/dl/dd/text()').extract_first()
            # if sick_introduce != None:
            #     sick_introduce = sick_introduce[2:]
            #
            # temp['sick_introduce'] = sick_introduce


            q = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[3]/ul/li[1]/i/text()').extract_first()
            q = q.replace('：','')

            q_1 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[3]//a/@title').extract()
            # q_1 = ''.join(q_1)

            temp[q]=q_1



            #疾病别名
            # temp['another_name'] = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[1]/text()').extract_first()
            #
            # #发病部位
            # temp['sick_site'] = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[3]/a/text()').extract()
            #
            # #是否属于医保
            # temp['is_yibao'] = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[2]/a/text()').extract_first()
            # print(response.url)
            next_url = response.xpath('/html/body/section/div[2]/div[3]/ul/li[2]/a/@href').extract_first()
            # print(temp)
            yield scrapy.Request(url=next_url,callback=self.next2,meta={'temp':temp})

    def next2(self,response):
        temp = response.meta['temp']

        sick_introduce = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[1]/dd/text()').extract_first()

        sick_introduce = sick_introduce.replace('\u3000\u3000','')


        temp['sick_introduce'] = sick_introduce


        next_url = temp['url'] + 'bfbz/'

        yield scrapy.Request(url=next_url,callback=self.next3,meta={'temp':temp})

    def next3(self,response):

        temp = response.meta['temp']

        temp['并发'] = response.xpath('/html/body/section/div[3]/div[1]/div/dl[2]/dd/a/@title').extract()


        yield temp
