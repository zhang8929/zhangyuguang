import urllib2
#coding:utf-8
if __name__ == '__main__':
    url_get_base = "http://ltpapi.voicecloud.cn/analysis/?"
    api_key = "L1m4c8G2H7Q4Y4t4F9e3uB5zbmJh4jaWJyLjAS5V"
    text=input("请输入句子：")
    while text!='exit' :
        format = "json"
        pattern = "ws"
        result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base, api_key, text, format, pattern))
        content = result.read().strip()
        print (content)
        text = input("请输入句子：")
    print "退出了"
