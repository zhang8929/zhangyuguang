#!/usr/bin/env python
# coding: utf-8

import sys
from pyhanlp import *

rs = "\
1	张三	张三	nh	nr	_	2	主谓关系	_	_\n\
2	出生于	出生于	v	v	_	0	核心关系	_	_\n\
3	四川	四川	ns	ns	_	2	动宾关系	_	_"

def  parse_CoNLL_format(s) :
    rs = {}
    ps = s.split("\n")
    for x in ps :
        words = x.split("\t")
        index = words[0]
        word = words[1]
        refer = words[6]
        ship  = words[7]
        type1 = words[3]
        type2 = words[4]

        index = int(index)
        m = {
            'word' : word,
            'index' : index,
            'refer' : refer,
            'rel'   : ship,
            'type1'  : type1,
            'type2'  : type2,
        }

        rs[index] = m

    return rs

rows = parse_CoNLL_format(rs)
print len(rows)

#for ws in rows :
#    print ws[0], ws[1], ws[3], ws[4], ws[6], ws[7]



