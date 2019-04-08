# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class EqPipeline(object):
	def __init__(self):
		self.f = open('/home/python/Desktop/eaq11111111.json', 'wb')

	def process_item(self, item, spider):

		jsontext = json.dumps(dict(item), ensure_ascii=False) + ',\n'

	# print(jsontext+'11111111111111111111111111111111111111111111111111111')
		self.f.write(jsontext.encode('utf-8'))
	#print(jsontext+str(11111111111111111111111111111111111111111111111111111111111111111111111))
		return item

	def close_spider(self, spider):

		self.f.close()

