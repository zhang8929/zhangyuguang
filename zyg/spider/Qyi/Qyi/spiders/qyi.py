# -*- coding: utf-8 -*-
import scrapy

with open('./url.json')as f:
    content = f.read().splitlines()



class QyiSpider(scrapy.Spider):
    name = 'qyi'
    allowed_domains = ['ci.qiuyi.cn']
    start_urls = ['http://ci.qiuyi.cn/']

    def parse(self, response):

        for i in content:
            yield scrapy.Request(url=i,callback=self.next)

    def next(self,response):
        temp = {}

        temp['症状名称'] = response.xpath('//*[@id="o_l"]/div[2]/h1/text()').extract_first()

        a = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[1]/strong/text()').extract_first()

        a = a.replace(':','')

        a_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[1]/span/text()').extract_first()

        temp[a] = a_1


        b = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[2]/strong/text()').extract_first()

        b = b.replace(':','')

        b_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[2]/span/text()').extract_first()

        temp[b] = b_1

        c = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[3]/strong/text()').extract_first()

        c = c.replace(':','')

        c_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[3]/span/text()').extract_first()

        temp[c] = c_1

        d = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[4]/strong/text()').extract_first()

        d = d.replace(':','')

        d_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[4]/span/text()').extract_first()

        temp[d] = d_1

        e = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[5]/strong/text()').extract_first()
        e = e.replace(':', '')

        e_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[5]/span/text()').extract_first()

        temp[e] = e_1
        try:
            f = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[6]/strong/text()').extract_first()
            f = f.replace(':', '')

            f_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[6]/span/text()').extract_first()

            temp[f] = f_1

        except:
            pass
        try:
            g = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[7]/strong/text()').extract_first()
            g = g.replace(':', '')

            g_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[7]/span/text()').extract_first()

            temp[g] = g_1
        except:
            pass
        try:
            h = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[8]/strong/text()').extract_first()
            h = h.replace(':', '')

            h_1 = response.xpath('//*[@id="o_l"]/div[2]/div[3]/ul/li[8]/span/text()').extract_first()

            temp[h] = h_1





        except:
            pass

        i = response.xpath('//*[@id="o_l"]/div[2]/div[2]/dl/dd[1]/a/text()').extract_first()

        i_1 = response.xpath('//*[@id="o_l"]/div[3]/p[2]/text()').extract_first()

        temp[i] = i_1
        try:
            temp['症状图片'] = response.xpath('//*[@id="o_l"]/div[3]/div/img/@src').extract_fitst()

        except:
            pass


        j = response.xpath('//*[@id="o_l"]/div[2]/div[2]/dl/dd[2]/a/text()').extract_first()

        j_1 = response.xpath('//*[@id="o_l"]/div[4]/p[2]/text()').extract_first()

        temp[j] = j_1

        k = response.xpath('//*[@id="o_l"]/div[2]/div[2]/dl/dd[3]/a/text()').extract_first()

        k_1 =''.join(response.xpath('//*[@id="o_l"]/div[5]/p/text()').extract())

        temp[k] = k_1

        temp['url'] = response.url

        l = response.xpath('//*[@id="o_l"]/div[2]/div[2]/dl/dd[4]/a/text()').extract_first()

        l_1 = ''.join(response.xpath('//*[@id="o_l"]/div[6]/p/text()').extract())

        temp[l] = l_1

        m = response.xpath('//*[@id="o_l"]/div[2]/div[2]/dl/dd[5]/a/text()').extract_first()

        m_1 = ''.join(response.xpath('//*[@id="o_l"]/div[7]/p/text()').extract())

        temp[m] = m_1














        yield temp
