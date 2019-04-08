#!/usr/bin/env python
# coding: utf-8
import json
import sys, os, time
import gensim
import logging

from flask import Flask
from flask import request

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

train_dir  = os.path.dirname(os.path.realpath(__file__)) +\
                        '';
train_path = "%s/%s" % (train_dir, 'fenci.txt')

model_dir  = os.path.dirname(os.path.realpath(__file__)) +\
                    '';

docs = {}
with open(train_path) as fh :
    index = 0
    for line in fh :
        l = line.strip()
        docs[index] = l
        index += 1
    fh.close()




model_name = "100w_100d_w15_m1_e400.bin"
model_path = "%s/%s" % (model_dir, model_name)
model_dm = gensim.models.Doc2Vec.load(model_path)
app = Flask(__name__)
@app.route('/index', methods=['GET', 'POST'])
def test():

    words = (request.args.get('words').encode('utf-8'))
    words = ((words).replace("'", '').split(' '))

    inferred_vector_dm = model_dm.infer_vector(doc_words=words)

    t0 = time.time()
    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)
    t1 = time.time()
    print "ORIG: %s\n--------" % ''.join(words)
    res = []
    for (i, sim) in sims :
        res.append([i,sim,docs[i]])
    result = {'result':res}
        # print "%d, %.04f, %s" % (i, sim, docs[i])
    # return "USED TIME: %.03f" % (t1 - t0)
    return json.dumps(result, ensure_ascii=False)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9199, debug=True)
