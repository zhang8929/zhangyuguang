# -*- coding: utf-8 -*-
import scrapy
import re

from selenium import webdriver


class QqmailSpider(scrapy.Spider):
    name = 'qqmail'
    allowed_domains = ['mail.qq.com']
    start_urls = ['http://en.mail.qq.com/cgi-bin/frame_html?sid=6t_o5gA_BCKGDhBM&r=dcedf209cd4fcc14a8a78ddaeeda628d']

    def start_requests(self):

        url = 'http://en.mail.qq.com/cgi-bin/frame_html?sid=6t_o5gA_BCKGDhBM&r=dcedf209cd4fcc14a8a78ddaeeda628d'

        data = {
        'u': '505865781@qq.com',
        'p': 'dddsssqqq0929',
        }  # 构造表单数据

        yield scrapy.FormRequest(url, formdata=data, callback=self.parse_page)


    def parse_page(self,response):
        print(response.url)

        mail_list = response.xpath('//*[@id="SysFolderList"]/ul/li[1]/a/@href').extract_first()
        print(mail_list)
        # print(response.text)