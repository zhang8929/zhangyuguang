# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# import random
# ip = ["123.7.177.20:9999", "59.33.46.156:6969","219.150.189.212:9999","221.182.89.234:63000","61.219.70.133:8080","59.127.38.117:8080"]  # 把类似这种形式的ip放到列表中
#
#
# class IPProxiesMiddleware(object):
#
#     def process_request(self, request, spider):
#         # 设置代理
#         #
#         # if "https" in request.url:
#         #     request.meta["proxy"] = 'https://{}'.format(random.choice(ip))  # https://127.0.0.1:8888
#         # else:
#         request.meta["proxy"] = 'http://{}'.format(random.choice(ip))  # http://127.0.0.1:8888
#
