#!/usr/bin/env python
# coding: utf-8

import os
from pyltp import SentenceSplitter
from intention import Intention

class FindKeys(object) :

    __db_dirname = ''
    __file_list  = []

    def __init__ (self) :

        self.__db_dirname = os.path.dirname(os.path.realpath(__file__))  +\
            '/../database/ignore/symptom'

        for fname in os.listdir(self.__db_dirname):
            self.__file_list.append("%s/%s" % (self.__db_dirname, fname))

    def test(self, maxFileCounts=1) :

        index = 0
        intention = Intention(False)
        for fname in self.__file_list :
            if maxFileCounts > 0 and index >= maxFileCounts :
                break
            (title, content) = self.__get_title_content(fname)

            print fname
            print title
            print '-' * 35

            cLines = 0
            for x in content :
                l =x.strip()
                intent = intention.get_intent(l)
                cLines += 1
                if cLines >= 3 :
                    break

            index += 1
            print "\n"

    def __get_title_content (self, fpath) :

        fh = open(fpath, 'r')
        ls = fh.readlines()
        fh.close()

        title = ls[0].strip()
        paragraph_list = ls[1:]
        sentence_list = []

        # 分句
        for paragraph in  paragraph_list :
            line = paragraph.strip()
            lines = SentenceSplitter.split(line)
            for sentence in lines :
                sentence_list.append(sentence)

        return (title, sentence_list)

if __name__ == '__main__' :

    find = FindKeys()
    find.test(30)

