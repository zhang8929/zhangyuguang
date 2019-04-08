
"""这里开始截图"""
# from selenium import webdriver
# import time
# driver = webdriver.Chrome('/Users/zhangyuan/Downloads/chromedriver')
#
# # browser = webdriver.Chrome()
# # driver.get('http://e.dangdang.com/pc/reader/index.html?id=1900465942')
# driver.get('http://www.dangdang.com/')
# time.sleep(100)
#
# driver.switch_to_window(driver.window_handles[1])
# time.sleep(5)
# pic_path = '/Users/zhangyuan/work/screen'
# while True:
#     for i in range(166):
#         driver.get_screenshot_as_file(pic_path+str(i)+'.png')
#         a = driver.find_element_by_id("ddclick-r-trun-right")
#         a.click()
#
# dirver.quit()

"""这里开始对图片批量截图"""
#方式一：质量不好
# import matplotlib.pylab as plt
#
# def plti(im, **kwargs):
#     """
#     画图的辅助函数
#     """
#     plt.imshow(im, interpolation="none", **kwargs)
#     plt.axis('off') # 去掉坐标轴
#     plt.show() # 弹窗显示图像
# # 加载图像
# for i in range (13,158):
#     file_path = "/Users/zhangyuan/work/screen/screen"+str(i)+'.png'
#     im = plt.imread(file_path)
#     print(im.shape)
#     im = im[100:2500,780:2100,:]  # 直接切片对图像进行裁剪
#     plti(im)

#方式二  OK
# from PIL import Image
# import os
#
# # 定义待批量裁剪的图像地址
# IMAGE_INPUT_PATH = '/Users/zhangyuan/work/screen'
# # 定义裁剪后的图像存放地址
# IMAGE_OUTPUT_PATH = '/Users/zhangyuan/work/screen_out'
# # 定义左，上，右和下像素坐标
# BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = 780, 100, 2100, 1700
#
# for each_image in os.listdir(IMAGE_INPUT_PATH):
#     # 每个图像全路径
#     image_input_fullname = IMAGE_INPUT_PATH + '/' + each_image
#     # PIL库打开每一张图
#     img = Image.open(image_input_fullname)
#
#     # 从此图像返回一个矩形区域。 盒子是一个4元组定义左，上，右和下像素坐标。
#     box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
#     # 进行ROI裁剪
#     roi_area = img.crop(box)
#     # 裁剪后每个图像全路径
#     image_output_fullname = IMAGE_OUTPUT_PATH + '/' + each_image.replace('screen','')
#     # 保存处理后的图像
#     roi_area.save(image_output_fullname)
#     print('{0} crop Done.'.format(each_image))


"""这里开始识别图片内容"""
# from aip import AipOcr
#
# """ 你的 APPID AK SK """
# APP_ID = '15841301'
# API_KEY = 'RGlR0zN4lCkXnoC6wxx21dgY'
# SECRET_KEY = 'hG3ZGd2PCdEwOoOI0vAnHKXLe6FIUfhT'
#
# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """

# import skimage.io as io
# from skimage import data_dir
# import os
#
# str='/Users/zhangyuan/work/menzhen_screen/*.png'
# coll = io.ImageCollection(str)
# data_base_dir = '/Users/zhangyuan/work/menzhen_screen'
#
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
# def ss(name):
#     return int(name.replace('.png',''))
#
# result = []
# name = os.listdir(data_base_dir)
# name.sort(key=ss)
#
# for xx in name:
#     # print(xx)
#     file_path = "/Users/zhangyuan/work/menzhen_screen/"+xx
#     img = get_file_content(file_path)
#     client.basicGeneral(img)
#
#     options = {}
#     options["language_type"] = "CHN_ENG"
#     options["detect_direction"] = "true"
#     options["detect_language"] = "true"
#     options["probability"] = "true"
#
#     """ 带参数调用通用文字识别, 图片参数为本地图片 """
#     a = client.basicGeneral(img, options)
#     result.append(a)
#     print(a)
#     with open('./menzhen.txt','a') as file:
#         file.write(a)
#         #TODO
#         # a = a + ','
#         file.write(a)
    # print(len(result))


import json
import re
str = ''
with open('/Users/zhangyuan/work/menzhen_jiankang.json', 'r') as file:
    content = file.read()
    print(type(content))
    data = json.loads(content)
    print(type(data))

    for dict in data:
        for row in dict['words_result']:
            rowrow = row['words'].replace('\n','')
            if re.search('第*节', row['words']) or re.search('疾病概述', rowrow):
                str += '\n'
            str += row['words']
    with open('./menzhen_jiankang_1.txt','w') as file:
        file.write(str)


with open('./menzhen_jiankang.txt','r') as file:
    content = file.readlines()
    print(len(content))
index = 0
while index < len(content)-1:
    # print(index)
    # print(content[index])
    # print(content[index][0])
    if len(content[index])==0:
        continue
    elif content[index][0] not in ['(',')','一','二','三','四','第'] :
        print(content[index])
        print('---------------')
        print(content[index-1])
        content[index] = content[index].replace('\n','')
        content[index-1] = content[index-1].replace('\n','')
        content[index-1] += content[index]
        del content[index]
        index -=1
    index += 1
# import json
# ll = json.dumps(content,ensure_ascii=False)
with open('./menzhen_jk.txt','w') as file:
    for dd in content:
        file.write(dd)

with open('./menzhen_jk.txt','r') as ff:
    content = ff.readlines()

for row in content:
    if row[0]==')':
        row.replace(')','(一)')
