#!/usr/bin/env python
# coding: utf-8
import pymysql
import jieba
import jieba.posseg as psg
# jieba.load_userdict('/mnt/flask/ci.txt')
# jieba.load_userdict('/home/python/Desktop/ci.txt')
jieba.load_userdict('/Users/zhangyuguang/Documents/data/ci.txt')

def get_data():
    connect = pymysql.Connect(
        host='154.8.214.203',
        port=3306,
        user='ai_dev',
        passwd='dev2018@centerai.cn',
        db='ccc_data',
        charset='utf8'
    )
    # connect = pymysql.Connect(
    #     host='localhost',
    #     port=3306,
    #     user='root',
    #     passwd='mysql',
    #     db='faq',
    #     charset='utf8'
    # )

    # 获取游标
    cursor = connect.cursor()

    sql = """select question,id from faq_user where fenci_q is null"""
    # sql = """select question from faq"""
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)

    for row in data:
        dd = row
        row = row[0]
        list1 = []
        for (word, flag) in psg.cut(''.join(row)):
            list1.append((word, flag))
        # print(list1)
        #
        list2 = []
        for i in list1:
            if i[1] != 'uj' and i[1] != 'x':
                list2.append(i[0])
        # print(list2)
        a = ' '.join(list2) + '\n'
        a = a[:-1]
        try:
            #nihao
            sql = """update faq_user set fenci_q='{}' where id={} """.format(a,dd[1])
            print(sql)
            cursor.execute(sql)
            connect.commit()


        except Exception as f:
            print(f)

    connect.close()

if __name__ == '__main__':
    get_data()