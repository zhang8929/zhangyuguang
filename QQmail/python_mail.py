# import requests
#
# # url = 'http://www.renren.com/PLogin.do'
# url = 'http://en.mail.qq.com/cgi-bin/frame_html?sid=6t_o5gA_BCKGDhBM&r=dcedf209cd4fcc14a8a78ddaeeda628d'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
# }
#
# data = {
#     'u':'505865781@qq.com',
#     'p':'dddsssqqq0929'
# }
#
# # 构造session对象，用来发送post请求，实现登录
# session = requests.Session()
#
# resp = session.post(url,headers=headers,data=data)
# print(resp.cookies)
# import re
# print(re.findall('张宇光',resp.content.decode()))

import time
from selenium import webdriver

url = 'http://en.mail.qq.com/cgi-bin/frame_html?sid=6t_o5gA_BCKGDhBM&r=dcedf209cd4fcc14a8a78ddaeeda628d'

driver = webdriver.Chrome('/Users/zhangyuguang/Downloads/chromedriver')

# 发送网络请求
driver.get(url)

# 模拟登录，qq空间使用的页面嵌套页面iframe，常规的提取数据的方法无法拿到数据
# 使用xpath定位内部iframe
iframe_mail = driver.find_element_by_xpath('//*[@id="login_frame"]')
# 找到内部iframe中，切换进去
driver.switch_to.frame(iframe_mail)

# 定位账号密码登录标签
switcher_plogin = driver.find_element_by_id('switcher_plogin')
switcher_plogin.click()

# 定位账号，发送qq账号
u = driver.find_element_by_id('u')
u.send_keys('505865781@qq.com')


p = driver.find_element_by_id('p')
p.send_keys('dddsssqqq0929')

# 点击登录按钮
login_button = driver.find_element_by_id('login_button')
login_button.click()

#点击收件箱按钮
time.sleep(6)
floder_button = driver.find_element_by_id('readmailbtn_link')
print(floder_button)
floder_button.click()

#遍历收件箱

floders_button = driver.find_elements_by_id('list')