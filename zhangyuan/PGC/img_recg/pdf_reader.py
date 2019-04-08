"""将pdf转成每页的图片"""
import pdf2image
print('start')
pages = pdf2image.convert_from_path('/Users/zhangyuan/Downloads/门诊患者健康教育手册_14180444.pdf')
print('over')

for i in range(0,len(pages)):
    print(i)
    pages[i].save(f'/Users/zhangyuan/work/menzhen_screen/{i+1}.png','PNG')
    print('wan')



