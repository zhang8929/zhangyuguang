# coding:utf-8
import sys
import gensim
import numpy as np
import json
import jieba
import time
from flask import Flask, request

app = Flask(__name__)
from gensim.models.doc2vec import Doc2Vec, LabeledSentence

TaggededDocument = gensim.models.doc2vec.TaggedDocument


class Nlp_handle():
    def __init__(self):


        self.read_txt()



        self.model_dm = Doc2Vec.load("./100w_100d_w15_m1_e400.bin",mmap='r')


    def read_txt(self):
        with open("./fenci.txt", 'r') as cf:

            self.docs = cf.readlines()



    def get_datasest(self):
        x_train = []

        # y = np.concatenate(np.ones(len(docs)))
        for i, text in enumerate(self.docs):
            word_list = text.split(' ')
            l = len(word_list)
            word_list[l - 1] = word_list[l - 1].strip()
            t1 = time.time()

            t2 = time.time()
            print t2 - t1


        return x_train

    def test(self, words_list):

        inferred_vector_dm = self.model_dm.infer_vector(words_list)
        # print inferred_vector_dm
        t0 = time.time()
        sims = self.model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)

        return sims

    def cut_word(self, words):
        words_list = []
        words = jieba.cut(words)
        for word in words:
            words_list.append(word)
        return words_list

    def main(self, words):
        x_train = self.get_datasest()

        # words_list = self.cut_word(words)
        # print(words_list)
        sims = self.test(words)

        res = []
        for count, sim in sims:
            sentence = x_train[count]
            words = ''
            for word in sentence[0]:
                words = words + word + ' '
            print (words, sim, len(sentence[0]))
            res.append([words, sim, len(sentence[0])])
        result = {'result': res}
        return json.dumps(result, ensure_ascii=False)


@app.route('/index', methods=['GET', 'POST'])
def index():
    words = (request.args.get('words').encode('utf-8'))
    words = ((words).replace("'", '').split(' '))
    print (words)
    # print words
    # print type(words)
    nlp_handle = Nlp_handle()
    result = nlp_handle.main(words)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6877, debug=True)

