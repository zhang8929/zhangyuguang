#!/usr/bin/env python
# coding: utf-8


import pymysql
import json
import jieba

import jieba.posseg as psg
import re

host = '127.0.0.1'
user = 'root'
passwd = 'mysql'
port = 3306
# db = 'faq'
db = 'FAQ'
class SelectMySQL(object):
    def __init__(self):
        jieba.load_userdict('/home/python/Desktop/new/ci.txt')

    def select_data(self,sql):
        result = []
        try:
            conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
            cur = conn.cursor()
            cur.execute(sql)
            alldata = cur.fetchall()

            for rec in alldata:

                result.append(rec[0])  # 注意，我这里只是把查询出来的第一列数据保存到结果中了,如果是多列的话，稍微修改下就ok了
        except Exception as e:
            # print('1111111111111111111111')
            print(e)
        # finally:
        #
        #     cur.close()
        #
        #     conn.close()


        return result

    def get_result(self, sql, filename):

        print(sql)
        results = self.select_data(sql)
        # print('The amount of datas: %d' % (len(results)))

        with open(filename, 'a+') as f:

            for result in results:
                result1 = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+',"",result)
                # print(result)
                list1 = []
                # words = ''

                for (word, flag) in psg.cut(result1):
                    list1.append((word, flag))
                    a = ''

                    for i in list1:
                        a += i[0]
                        a += ' '

                f.write(str(a) + '\n')

        # print('Data write is over!')

        return results

if __name__ == '__main__':
    # for i in range(6380098):
    sql = "select question from youlayi_all where id<7854429;"

        # sql = sql1 + str(i) + ';'

    select = SelectMySQL()

    result1 = select.get_result(sql, 'aq.txt')

    print(result1)








