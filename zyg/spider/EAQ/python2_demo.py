#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import requests
import json
import hashlib
import base64

#接口地址
url ="http://ltpapi.xfyun.cn/v1/cws"
#开放平台应用ID
x_appid = "5c0f2610"
#开放平台应用接口秘钥
api_key = "db49b91fffa91e1ba9c4a028f987e575"
#语言文本
TEXT=u"汉皇重色思倾国，御宇多年求不得。杨家有女初长成，养在深闺人未识。天生丽质难自弃，一朝选在君王侧。"


def main():
    body = {'text': TEXT}

    param = {"type": "dependent"}

    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {"Content-Type": "application/x-www-form-urlencoded",
                'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = requests.post(url, body, headers=x_header)

    result = req.content
    print result.decode('utf-8')
    return

if __name__ == '__main__':
    main()
