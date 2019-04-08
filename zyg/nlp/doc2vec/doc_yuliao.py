import pymysql.cursors
import jieba
import jieba.posseg as psg
#加载结巴自定义词典
jieba.load_userdict("/Users/zhangyuguang/Documents/data/ci.txt")
# 连接数据库
connect = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='mysql',
#     db='faq',
#     charset='utf8'
# )
host = '154.8.214.203',
port = 3306,
user = 'ai_dev',
passwd = 'dev2018@centerai.cn',
db = 'ccc_data',
charset = 'utf8')
# 获取游标
cursor = connect.cursor()


sql = "SELECT question FROM faq_new WHERE id <'%s'  AND Level_1_department in ('男科', '性病科', '分娩', '不孕不育', '备孕', '产后', '两性健康 ', '女性不孕', '男性不孕', '生殖疾病', '妇幼保健科', '生殖医学科', '性功能', '性生活', '计划生育科', '计划生育', '男科学', '妇产科', '月经不调', '产前诊断科', '母婴 ', '母婴', '孕期', '产科', '妇科肿瘤', '妇科内分泌', '肿瘤妇科', '性教育', '妇科') OR Level_2_department in ('男科', '性病科', '分娩', '不孕不育', '备孕', '产后', '两性健康 ', '女性不孕', '男性不孕', '生殖疾病', '妇幼保健科', '生殖医学科', '性功能', '性生活', '计划生育科', '计划生育', '男科学', '妇产科', '月经不调', '产前诊断科', '母婴 ', '母婴', '孕期', '产科', '妇科肿瘤', '妇科内分泌', '肿瘤妇科', '性教育', '妇科')"
data = ('11100001')

cursor.execute(sql % data)
print(sql)
f = open('/Users/zhangyuguang/Documents/data/007.txt','wb+')
for row in cursor.fetchall():
    # print(row)
    list1 = []
    for (word, flag) in psg.cut(''.join(row)):
        list1.append((word,flag))
    # print(list1)

    list2 = []
    for i in list1:
        if i[1]!='uj' and i[1]!='x':
            list2.append(i[0])
    # print(list2)
    a = ' '.join(list2) + '\n'
    print(a)


    f.write(a.encode('utf-8'))
print('共查找出', cursor.rowcount, '条数据')
