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

        ###
        sick_introduce = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[1]/dd/text()').extract()
        sick_introduce = ''.join(sick_introduce)

        temp['sick_introduce'] = sick_introduce
        print(response.url)

        z = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[1]/i/text()').extract_first()
        if z != None:
            z = z[:-1]
        z_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[1]/text()').extract()
        temp[z] = ((''.join(z_1)).replace('\r\n','')).strip()
        temp['name'] = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dt/text()').extract_first()

        y = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[2]/i/text()').extract_first()
        if y != None:
            y = y[:-1]
        y_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[2]/text()').extract()
        temp[y] = ((''.join(y_1)).replace('\r\n', '')).strip()

        x = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[3]/i/text()').extract_first()
        if x != None:
            x = x[:-1]
        x_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[1]/text()').extract()
        temp[x] = ((''.join(x_1)).replace('\r\n', '')).strip()

        w = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[4]/i/text()').extract_first()
        if w != None:
            w = w[:-1]
        w_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[4]/text()').extract()
        temp[w] = ((''.join(w_1)).replace('\r\n', '')).strip()





        a = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[1]/i/text()').extract_first()
        if a != None:
            a = a.replace('：', '')

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[1]/a/text()').extract()
        # temp[a] = ((''.join(a_1)).replace('\r\n', '')).strip()
        # if ''.join(a_1) == '':
        #     a_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[1]/text()').extract()
        #     temp[a] = a_2
        # else:
        temp[a] = a_1

        b = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[2]/i/text()').extract_first()
        if b != None:
            b = b.replace('：', '')
        b_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[2]/text()').extract()
        # temp[b] = ((''.join(b_1)).replace('\r\n', '')).strip()

        # if ''.join(b_1) == '':
        #     b_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[2]/text()').extract()
        #     temp[b] = b_2
        # else:
        temp[b] = b_1

        c = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[3]/i/text()').extract_first()
        if c != None:
            c = c.replace('：', '')
        c_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[3]/a/text()').extract()
        # temp[c] = ((''.join(c_1)).replace('\r\n', '')).strip()

        # if ''.join(c_1) == '':
        #     c_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[3]/text()').extract()
        #     temp[c] = c_2
        # else:
        temp[c] = c_1

        d = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[4]/i/text()').extract_first()
        if d != None:
            d = d.replace('：', '')
        d_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[4]/text()').extract()

        # temp[d] = ((''.join(d_1)).replace('\r\n', '')).strip()

        # if ''.join(d_1) == '':
        #     d_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[4]/text()').extract()
        #     temp[d] = d_2
        # else:
        temp[d] = d_1

        e = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[5]/i/text()').extract_first()
        if e != None:
            e = e.replace('：', '')
        e_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[5]/text()').extract()

        # temp[e] = ((''.join(e_1)).replace('\r\n', '')).strip()

        # if ''.join(e_1) == '':
        #     e_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[5]/text()').extract()
        #     temp[e] = e_2
        # else:
        temp[e] = e_1

        f = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[6]/i/text()').extract_first()
        if f != None:
            f = f.replace('：', '')
        f_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[6]/text()').extract()

        # temp[f] = ((''.join(f_1)).replace('\r\n', '')).strip()

        # if ''.join(f_1) == '':
        #     f_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[6]/text()').extract()
        #     temp[f] = f_2
        # else:
        temp[f] = f_1

        g = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[7]/i/text()').extract_first()
        if g != None:
            g = g.replace('：', '')

        g_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[7]/text()').extract()

        # temp[g] = ((''.join(g_1)).replace('\r\n', '')).strip()

        # if ''.join(g_1) == '':
        #     g_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[7]/text()').extract()
        #     temp[g] = g_2
        # else:
        temp[g] = g_1

        h = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[8]/i/text()').extract_first()
        if h != None:
            h = h.replace('：', '')
        h_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[8]/text()').extract()
        # temp[h] = ((''.join(h_1)).replace('\r\n', '')).strip()

        # if ''.join(h_1) == '':
        #     h_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[8]/text()').extract()
        #     temp[h] = h_2
        # else:
        temp[h] = h_1

        i = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[9]/i/text()').extract_first()
        if i != None:
            i = i.replace('：', '')
        i_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[9]/text()').extract()

        # temp[i] = ((''.join(i_1)).replace('\r\n', '')).strip()

        # if ''.join(i_1) == '':
        #     i_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[9]/text()').extract()
        #     temp[i] = i_2
        # else:
        temp[i] = i_1

        j = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[10]/i/text()').extract_first()
        if j != None:
            j = j.replace('：', '')
        j_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[10]/a/text()').extract()

        # temp[j] = ((''.join(j_1)).replace('\r\n', '')).strip()

        # if ''.join(j_1) == '':
        #     j_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[10]/text()').extract()
        #     temp[j] = j_2
        # else:
        temp[j] = j_1

        k = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[11]/i/text()').extract_first()
        if k != None:
            k = k.replace('：', '')
        k_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[11]/a/text()').extract()

        # temp[k] = ((''.join(k_1)).replace('\r\n', '')).strip()

        # if ''.join(k_1) == '':
        #     k_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[11]/text()').extract()
        #     temp[k] = k_2
        # else:
        temp[k] = k_1

        l = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[1]/i/text()').extract_first()
        if l != None:
            l = l.replace('：', '')
        l_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[1]/a/text()').extract()
        # temp[l] = ((''.join(l_1)).replace('\r\n', '')).strip()
        #
        # if ''.join(l_1) == '':
        #     l_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[12]/text()').extract()
        #     temp[l] = l_2
        # else:
        temp[l] = l_1

        m = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[2]/i/text()').extract_first()
        if m != None:
            m = m.replace('：', '')
        m_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[2]/a/text()').extract()

        # temp[m] = ((''.join(m_1)).replace('\r\n', '')).strip()
        #
        # if ''.join(m_1) == '':
        #     m_2 = response.xpath('/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[13]/text()').extract()
        #     temp[m] = m_2
        # else:
        temp[m] = m_1

        n = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[3]/i/text()').extract_first()
        if n != None:
            n = n.replace('：', '')
        n_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[3]/text()').extract()

        # temp[n] = ((''.join(n_1)).replace('\r\n', '')).strip()
        #
        # if ''.join(n_1) == '':
        #     n_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[14]/text()').extract()
        #     temp[n] = n_2
        # else:
        temp[n] = n_1

        o = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[4]/i/text()').extract_first()
        if o != None:
            o = o.replace('：', '')
        o_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[4]/text()').extract()
        # temp[o] = ((''.join(o_1)).replace('\r\n', '')).strip()

        # if ''.join(o_1) == '':
        #     o_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[15]/text()').extract()
        #     temp[o] = o_2
        # else:
        temp[o] = o_1

        p = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[5]/i/text()').extract_first()
        if p != None:
            p = p.replace('：', '')
        p_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[5]/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[p] = p_1

        q = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[6]/i/text()').extract_first()
        if q != None:
            q = q.replace('：', '')
        q_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[6]/a/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[q] = q_1

        r = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[7]/i/text()').extract_first()
        if r != None:
            r = r.replace('：', '')
        r_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[7]/a/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[r] = r_1

        s = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[1]/i/text()').extract_first()
        if s != None:
            s = s.replace('：', '')
        s_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[1]/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[s] = s_1

        t = response.xpath('//html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[2]/i/text()').extract_first()
        if t != None:
            t = s.replace('：', '')
        t_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[2]/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[t] = t_1

        u = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[3]/i/text()').extract_first()
        if u != None:
            u = u.replace('：', '')
        u_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[3]/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[u] = u_1

        v = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[4]/i/text()').extract_first()
        if v != None:
            v = v.replace('：', '')
        v_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[4]/text()').extract()

        # temp[p] = ((''.join(p_1)).replace('\r\n', '')).strip()

        # if ''.join(p_1) == '':
        #     p_2 = response.xpath(
        #         '/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[16]/text()').extract()
        #     temp[p] = p_2
        # else:
        temp[v] = v_1

        next_url = temp['url']+'zztz/'
        # print(temp)
        yield scrapy.Request(url=next_url,callback=self.next3,meta={'temp':temp})

    def next3(self,response):
        temp = response.meta['temp']
        a = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dt/text()').extract_first()
        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[1]/text()').extract()
        a_1 = (''.join(a_1)).strip()
        temp[a] = a_1

        eee = response.xpath('/html/body/section/div[3]/div[1]/div[1]/div[2]//text()').extract()
        eee = (''.join(eee)).strip()
        temp['病症'] = eee

        next_url = temp['url'] + 'blby/'

        yield scrapy.Request(url=next_url,callback=self.next4,meta={'temp':temp})

    def next4(self,response):
        temp = response.meta['temp']

        a = '病因'

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div/div[2]//text()').extract()
        a_1 = (''.join(a_1)).strip()

        temp[a] = a_1

        next_url = temp['url'] + 'yfhl/'

        yield scrapy.Request(url=next_url,callback=self.next5,meta={'temp':temp})

    def next5(self,response):

        temp = response.meta['temp']

        a = '预防'

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div/div[2]//text()').extract()

        a_1 = (''.join(a_1)).strip()
        temp[a] = a_1
        next_url = temp['url'] + 'jcjb/'
        yield scrapy.Request(url=next_url,callback=self.next6,meta={'temp':temp})

    def next6(self,response):
        temp = response.meta['temp']

        a = '检查'

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/div[3]//text()').extract()
        a_1 = (''.join(a_1)).strip()

        temp[a] = a_1

        next_url = temp['url'] + 'jb/'
        yield scrapy.Request(url=next_url,callback=self.next7,meta={'temp':temp})

    def next7(self,response):

        temp = response.meta['temp']

        a = '鉴别'

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/div[2]//text()').extract()

        a_1 = (''.join(a_1)).strip()

        temp[a] = a_1

        next_url = temp['url'] + 'yyzl/'

        yield scrapy.Request(url=next_url,callback=self.next8,meta={'temp':temp})

    def next8(self,response):
        temp = response.meta['temp']

        a = '治疗'

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/div[2]//text()').extract()

        a_1 = (''.join(a_1)).strip()

        temp[a] = a_1

        next_url = temp['url'] + 'hl/'

        yield scrapy.Request(url=next_url,callback=self.next9,meta={'temp':temp})

    def next9(self,response):

        temp = response.meta['temp']

        a = '护理'
        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/div[2]//text()').extract()
        a_1 = (''.join(a_1)).strip()

        temp[a] = a_1


        next_url = temp['url'] + 'ysbj/'

        yield scrapy.Request(url=next_url,callback=self.next10,meta={'temp':temp})

    def next10(self,response):

        temp = response.meta['temp']

        a = '饮食保健'

        a_1 = response.xpath('/html/body/section/div[3]/div[1]/div[1]/div[4]//text()').extract()

        a_1 = (''.join(a_1)).strip()

        temp[a] = a_1

        # next_url1 = temp['url'] + 'jbzs/'
        # # print(temp)
        # # print(next_url1)
        #
        # yield scrapy.Request(url=next_url1,callback=self.detaill,meta={'temp':temp})
    #
    # def detaill(self,response):
    #     print('*'*10011)
    #     temp = response.meta['temp']


        # print(response.url)





        # print(temp)









        yield temp




