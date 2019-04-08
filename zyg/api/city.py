#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,request
# import sys

import json

app = Flask(__name__)


@app.route('/index', methods=['GET','POST'])
def fun():
    city = request.args.get('city', None)
    if city[0] != u'(' and city[-1] == u'市':
        #
        # dic={}
        # dic['city']=city[:-1]
        t = {'state': None, 'pro': None, 'city': city[:-1]}

        return json.dumps(t, ensure_ascii=False)

    if city[0] != u'(' and city[-1] == u'省':
        t = {'state': None, 'pro': city[:-1], 'city': None}
        return json.dumps(t, ensure_ascii=False)
    if city[0] != u'(' and city[-1] != u'市' and city[-1] != u'区' and city[-1] != u'省':
        t = {'state': None, 'pro': None, 'city': city}
        return json.dumps(t, ensure_ascii=False)
    if city[0] != u'(' and city[-3:] == u'行政区':
        t = {'state': None, 'pro': city[-7:-5], 'city': None}
        return json.dumps(t, ensure_ascii=False)
    if city[0] != u'(' and city[-3:] == u'自治区':
        t = {'state': None, 'pro': city[:2], 'city': None}
        return json.dumps(t, ensure_ascii=False)

    if city[0] == u'(' and city[-1] == u'省':
        t = {'state': city[1:3], 'pro': city[:-1], 'city': None}
        return json.dumps(t, ensure_ascii=False)
    if city[0] == u'(' and city[-1] == u'市':
        t = {'state': None, 'pro': city[1:3], 'city': city[-3:-1]}
        return json.dumps(t, ensure_ascii=False)
    if city[0] == u'(' and city[-1] == u'州':
        t = {'state': None, 'pro': city[1:3], 'city': city[6:8]}
        return json.dumps(t, ensure_ascii=False)

    if city[0] == u'(' and city[-1] != u'州' and city[-1] != u'市' and city[-1] != u'省':
        if city[-3] == '>':
            t = {'state': city[1:3], 'pro': None, 'city': city[-2:]}
            return json.dumps(t, ensure_ascii=False)
        if city[-4] == '>':
            t = {'state': city[1:3], 'pro': None, 'city': city[-3:]}
            return json.dumps(t, ensure_ascii=False)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8999', debug=False)

