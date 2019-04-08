import pymysql.cursors
import time
local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 连接数据库
connect = pymysql.Connect(
    host='154.8.214.203',
    port=3306,
    user='ai_dev',
    passwd='dev2018@centerai.cn',
    db='ccc_data',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()

#取出被标记为未更新的内容
sql = "SELECT * FROM news_info1 WHERE is_copy=0 limit 10"

cursor.execute(sql)
connect.commit()

a = cursor.fetchall()

try:
    for i in a :
        print(i)
        sql1 = 'update news_info1 set is_copy = 1 WHERE id=%d'%i[3]
        # print(sql1)
        sql2 = 'insert into news_info(create_time,update_time,pic,title,summary,source,context,click_count,status,category_id,user_id,update_t)'\
            'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
            %(i[0],i[1],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[13],i[14],local_time)
        # print(sql2)
        cursor.execute(sql1)
        cursor.execute(sql2)

        connect.commit()

except Exception as f:
    print(f)
