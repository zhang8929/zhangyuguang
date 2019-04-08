# -*- coding: utf-8 -*-
import scrapy


class Zz39Spider(scrapy.Spider):
    name = 'zz39'
    allowed_domains = ['jbk.39.net']
    start_urls = ['http://jbk.39.net/']

    def parse(self, response):
        search_url = 'http://jbk.39.net/bw_t2_p'

        for i in range(201):
            link = search_url + str(i)

            yield scrapy.Request(url=link, callback=self.detail)

    def detail(self,response):

        node_list = response.xpath('//*[@id="res_subtab_1"]/div/dl/dt/h3/a/@href').extract()

        for node in node_list:
            yield scrapy.Request(url=node,callback=self.next1)

    def next1(self,response):
        temp = {}

        temp['症状名称'] = response.xpath('/html/body/section[1]/header/div[1]/a/h1/text()').extract_first()

        temp['image_url'] = response.xpath('/html/body/section[1]/div[2]/article/div[1]/div[1]/a/img/@src').extract_first()

        temp['简介'] = response.xpath('//*[@id="intro"]/p/text()').extract_first()
        temp['url'] = response.url

        temp['分类'] = response.xpath('/html/body/section[1]/div[2]/article/div[1]/div[2]/div[2]/table//tr/td[1]/a/@title').extract()

        temp['可能'] = response.xpath('/html/body/section[1]/div[2]/article/div[1]/div[2]/div[2]/table//tr/td[1]/a/@title').extract()

        temp['药品'] = response.xpath('/html/body/section[1]/div[2]/article/div[3]/div[2]/dl/dd/h4/a/@title').extract()


        link = temp['url'] + 'zzqy/'

        yield scrapy.Request(url=link,callback=self.next2,meta={'temp':temp})

    def next2(self,response):

        temp = response.meta['temp']

        temp['症状起因'] = ((''.join(response.xpath('/html/body/section/div[2]/article/div/div[2]/div[1]//text()').extract())).replace('\r\n','')).strip()

        link = temp['url'] + 'zdxs/'

        yield scrapy.Request(url=link,callback=self.next3,meta={'temp':temp})

    def next3(self,response):

        temp = response.meta['temp']

        temp['诊断详述'] = ((''.join(response.xpath('/html/body/section/div[2]/article/div/div[2]/div[1]//text()').extract())).replace('\r\n','')).strip()

        link = temp['url'] + 'jcjb/'


        yield scrapy.Request(url=link,callback=self.next4,meta={'temp':temp})

    def next4(self,response):

        temp = response.meta['temp']

        temp['检查名称'] = response.xpath('/html/body/section/div/article/div/div/div/div/div/table//tr/td[1]/a/text()').extract()

        temp['相似症状'] = response.xpath('/html/body/section/div[2]/article/div/div[2]/div[2]/div/ul/li/dl/dt/a/@title').extract()
        # print(response.url)
        # print(temp['相似症状'])
        link = temp['url'] + 'jzzn/'

        yield scrapy.Request(url=link,callback=self.next5,meta={'temp':temp})

    def next5(self,response):

        temp = response.meta['temp']

        a = response.xpath('/html/body/section/div[2]/article/div/div/div/dl[1]/dt/text()').extract_first()

        a_1 = response.xpath('/html/body/section/div[2]/article/div/div/div/dl[1]/dd/text()').extract()

        temp[a] = a_1

        b = response.xpath('/html/body/section/div[2]/article/div/div/div/dl[2]/dt/text()').extract_first()

        b_1 = (''.join(response.xpath('/html/body/section/div[2]/article/div/div/div/dl[2]/dd/text()').extract())).strip()

        temp[b] = b_1



        c = response.xpath('/html/body/section/div[2]/article/div/div/div/dl[3]/dt/text()').extract_first()

        c_1 = (''.join(response.xpath('/html/body/section/div[2]/article/div/div/div/dl[3]/dd/text()').extract())).strip()

        temp[c] = c_1

        d = response.xpath('/html/body/section/div[2]/article/div/div/div/dl[4]/dt/text()').extract_first()

        d_1 = (''.join(response.xpath('/html/body/section/div[2]/article/div/div/div/dl[4]/dd/text()').extract())).strip()

        temp[d] = d_1

        e = response.xpath('/html/body/section/div[2]/article/div/div/div/dl[5]/dt/text()').extract_first()

        e_1 = (
        ''.join(response.xpath('/html/body/section/div[2]/article/div/div/div/dl[5]/dd/text()').extract())).strip()

        temp[e] = e_1



        yield temp

        # print(len(node_list))

