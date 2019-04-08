#!/usr/bin/env python
# coding: utf-8
from triple_extraction import *
import json

extractor = TripleExtractor()

# content = "如果血管中脂肪不断沉积就会形成斑块。斑块若发生在冠状动脉就会导致其收缩进一步减少其对心肌的供血就形成了冠心病。冠状动脉内脂肪不断沉积逐渐形成斑块的过程称为冠状动脉硬化。一些斑块比较坚硬而稳定就会导致冠状动脉本身的缩窄和硬化。"
# content = '心电图是诊断心肌缺血的最常用的无创性检查，静息时心电图在正常范围内的患者可考虑进行动态心电图记录和（或）心脏负荷试验。'
with open('answer1','r',encoding='utf-8') as f:
    text_line = f.readline().strip()
    num=1
    L =[]
    while text_line:
        svos = extractor.triples_main(text_line)
        dict={'con':text_line,'svos':svos}
        L.append(dict)
        text_line = f.readline().strip()#继续读取一行
        num+=1

jsL = json.dumps(L, ensure_ascii=False)

with open('ans_cq3t.json', 'wb') as ff:
    ff.write(jsL.encode('utf-8'))


