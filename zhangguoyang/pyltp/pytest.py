#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,request
import json
import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import urllib2
app = Flask(__name__)
@app.route('/index', methods=['GET','POST'])

def fun():
	zi = request.args.get('words', None)
	zi = zi.encode('utf-8')
	response = urllib2.Request('http://154.8.214.203:9999/index?words='+zi)
	res = urllib2.urlopen(response)
	hjson = res.read()
	
	hjson = json.loads(hjson,'utf-8') 
	word = []
	tag = []

	for i in hjson['result']:

       		word.append(i[0].encode('utf-8'))
       		tag.append(i[1].encode('utf-8'))
	LTP_DATA_DIR = '/root/ltp_data_v3.4.0'  # ltp模型目录的路径
	#cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
	#pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
	par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')

	#segmentor = Segmentor()  # 初始化实例
	#postagger = Postagger()
	parser = Parser()

	#segmentor.load_with_lexicon(cws_model_path,'/root/pyltp/ci.txt')  # 加载模型
	#postagger.load(pos_model_path)
	parser.load(par_model_path)

	#words = segmentor.segment(zi)  # 分词
	#postags = postagger.postag(words)
	arcs = parser.parse(word,tag)

	#w=[]
	#for x in words:
		#w.append(x)
	#p=[]
	#for v in postags:
		#p.append(v)
	a = []
	for pr in arcs:
		zi = {}
		zi['head']=pr.head
		zi['relation']=pr.relation
		a.append(zi)
	#print type(arcs)
	#print '\t'.join(words)
	#print '\t'.join(postags)
	#print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)

	for k,i in enumerate(a):
		i['words']=word[k]
		i['tag']=tag[k]

	#segmentor.release()  # 释放模型
	#postagger.release()
	parser.release() 
	#print i
	#result = {'result':a}
	return json.dumps(a,ensure_ascii=False)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=14766, debug=True)
