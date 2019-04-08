# -*- coding: utf-8 -*-
import scrapy


class Jc120Spider(scrapy.Spider):
    name = 'jc120'
    allowed_domains = ['tag.120ask.com']
    start_urls = ['http://tag.120ask.com/']

    def parse(self, response):
        search_url = 'http://tag.120ask.com/shoushu/pinyin.html'

        yield scrapy.Request(url=search_url,callback=self.next1)

    def next1(self,response):
        node_list= response.xpath('//*[@class="w_bing"]/li/a/@href').extract()

        for node in node_list:
            link = 'http://tag.120ask.com' + node

            yield scrapy.Request(url=link,callback=self.next2)

    def next2(self,response):
        temp = {}

        temp['手术名称'] = response.xpath('//*[@class="w_n"]/h3/text()').extract_first()

        temp['部位'] = response.xpath('//*[@class="w_span"]/a/text()').extract()

        temp['科室'] = response.xpath('//*[@class="w_d1"]/span[2]/a/text()').extract_first()

        temp['手术方式'] = response.xpath('//*[@class="w_d2"]/span[1]/text()').extract_first().replace('手术方式：','')

        temp['麻醉'] = response.xpath('//*[@class="w_d2"]/span[2]/text()').extract_first().replace('麻醉：','')

        # temp['简介'] = response.xpath('/html/body/div[7]/div[1]/dl/dd[3]/span/text()').extract_first()


        temp['url'] = response.url

        next_url = response.url.replace('.html','/shiying.html')

        yield scrapy.Request(url=next_url,callback=self.next3,meta={'temp':temp})

    def next3(self,response):
        print(response.url)
        temp = response.meta['temp']
        temp['适应症'] = (''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\u3000','')

        next_url = temp['url'].replace('.html', '/bingfa.html')
        yield scrapy.Request(url=next_url, callback=self.next4, meta={'temp': temp})

    def next4(self,response):
        temp = response.meta['temp']

        temp['并发症'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t','')).replace('\u3000','')

        next_url = temp['url'].replace('.html', '/jinji.html')
        yield scrapy.Request(url=next_url, callback=self.next5, meta={'temp': temp})

    def next5(self,response):
        temp = response.meta['temp']
        temp['手术禁忌'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t','')).replace('\u3000','')

        next_url = temp['url'].replace('.html', '/buzhou.html')
        yield scrapy.Request(url=next_url, callback=self.next6, meta={'temp': temp})

    def next6(self,response):
        temp = response.meta['temp']
        temp['手术步骤'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t','')).replace('\u3000','')

        next_url = temp['url'].replace('.html', '/zhunbei.html')
        yield scrapy.Request(url=next_url, callback=self.next7, meta={'temp': temp})

    def next7(self, response):
        temp = response.meta['temp']
        temp['术前准备'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t', '')).replace('\u3000', '')

        next_url = temp['url'].replace('.html', '/huli.html')
        yield scrapy.Request(url=next_url, callback=self.next8, meta={'temp': temp})

    def next8(self, response):
        temp = response.meta['temp']
        temp['术后护理'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t', '')).replace('\u3000', '')

        next_url = temp['url'].replace('.html', '/zhuyi.html')
        yield scrapy.Request(url=next_url, callback=self.next9, meta={'temp': temp})

    def next9(self, response):
        temp = response.meta['temp']
        temp['注意事项'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t', '')).replace('\u3000', '')

        next_url = temp['url'].replace('.html', '/baojia.html')
        yield scrapy.Request(url=next_url, callback=self.next10, meta={'temp': temp})

    def next10(self,response):
        temp = response.meta['temp']

        temp['手术报价'] = ((''.join(response.xpath('//*[@class="w_contl fl"]/p/text()').extract())).replace('\t', '')).replace('\u3000', '')

        yield temp