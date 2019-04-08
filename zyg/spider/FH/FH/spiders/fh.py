# -*- coding: utf-8 -*-
import scrapy
with open('./url.json','r')as f:
    content = f.read().splitlines()


class FhSpider(scrapy.Spider):
    name = 'fh'
    allowed_domains = ['zzk.fh21.com.cn']
    start_urls = ['http://zzk.fh21.com.cn']

    def parse(self, response):

        for i in content:
            link ='http://zzk.fh21.com.cn' + i

            print(link)

            yield scrapy.Request(url=link,callback=self.next1)

    def next1(self,response):
        temp = {}
        temp ['症状名称'] = response.xpath('//*[@class="submenu"]/ul/div/h2/strong/a/text()').extract_first()

        temp['简介'] = (((''.join(response.xpath('//*[@class="main_content"]/ul/dl/dd/text()').extract())).replace('\r\n','')).replace('\t','')).strip()

        temp['image_link'] = response.xpath('//*[@class="z_block06a"]/dt/a/img/@src').extract_first()

        temp['科室'] = response.xpath('//*[@class="z_block07"]/div[1]/dl/dd/span/a/text()').extract()

        temp['发病部位'] = response.xpath('//*[@class="z_block07"]/div[2]/dl/dd/a/text()').extract()
        temp['易发人群'] = response.xpath('//*[@class="z_block07"]/dl/dd/text()').extract_first()

        a = (response.xpath('//*[@class="z_block07"]/div[3]/dl/dt/text()').extract_first()).replace('：','')
        if a !=None:
            temp[a] = response.xpath('//*[@class="z_block07"]/div[3]/dl/dd/a/@title').extract()

        try:
            b = (response.xpath('//*[@class="z_block07"]/div[4]/dl/dt/text()').extract_first()).replace('：','')
            if b!=None:
                temp[b] = response.xpath('//*[@class="z_block07"]/div[4]/dl/dd/a/@title').extract()
            else:
                pass
        except:
            pass

        temp['检查项目'] = response.xpath('//*[@class="z_block07"]/div[4]/dl/dd/a/span/text()').extract()

        temp['url'] = response.url



        yield temp