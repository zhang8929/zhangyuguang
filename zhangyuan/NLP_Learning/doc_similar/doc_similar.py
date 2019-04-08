# import jieba.analyse
# import numpy as np
# import jieba
#
# # jieba.load_userdict("userdict.txt")
#
# def cos_sim(vector_a, vector_b):
#     """
#     计算两个向量之间的余弦相似度
#     :param vector_a: 向量 a
#     :param vector_b: 向量 b
#     :return: sim
#     """
#     print(vector_a,vector_b)
#     vector_a = np.mat(vector_a)
#     vector_b = np.mat(vector_b)
#     num = float(vector_a * vector_b.T)
#     denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
#     cos = num / denom
#     sim = 0.5 * cos
#     return sim
#
#
# a = '你是机器人吗'
# b = ['您好医生',
#      '医生在吗']
#
# '''提取关键词'''
# # a_list = jieba.analyse.extract_tags(a, withWeight=True, topK=20) #list 关键词list
# # list_a = []
# # for a in a_list:
# #     list_a.append(a[0])
#
# list_a = ' '.join(jieba.cut(a))
# print(list_a)
#
#
# res = []
# for x in b:
#     c = []
#     '''提取关键词'''
#     # b_list = jieba.analyse.extract_tags(x, withWeight=True, topK=20) #list 关键词list
#     # list_b = []
#     #
#     # for b in b_list:
#     #     list_b.append(b[0])
#
#     list_b = ' '.join(jieba.cut(x))
#     print(list_b)
#
#     c = list(set(list_a + list_b))
#     # print(c)
#
#     num_a = []
#     num_b = []
#     for j in c:
#         a_nub = list_a.count(j)
#         num_a.append(a_nub)
#         b_num = list_b.count(j)
#         num_b.append(b_num)
#
#     similarity = cos_sim(num_a,num_b)
#     t = (x,similarity)
#     res.append(t)
#
# def takeSecond(f):
#     return f[1]
#
# res.sort(key=takeSecond,reverse=True)
#
# print(res)

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pymysql
from flask import Flask,request,jsonify
app=Flask(__name__)

def get_data():
    host= '154.8.214.203'
    user= 'ai_dev'
    password = 'dev2018@centerai.cn'
    db = 'ccc_data'
    db = pymysql.connect(host, user, password, db)
    cursor = db.cursor()
    sql = """select content from b_chat_free """
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

def takeSecond(f):
    return f[1]


def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    res = 1.0 * numerator / denominator
    return "%.3f" % res

@app.route('/',methods=['GET','POST'])
def res():
    res = []
    word = request.args.get('words')
    data = get_data()
    for dd in data:
        value = jaccard_similarity(word,dd[0])
        # print(type(value))
        if float(value) < 0.25:
            continue
        tmp = (dd,value)
        res.append(tmp)

    res.sort(key=takeSecond, reverse=True)
    if len(res)>=1:
        return jsonify(res=res[0])
    else:
        return jsonify('')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)