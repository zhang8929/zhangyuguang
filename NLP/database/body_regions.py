# coding: utf-8

import os


# 身体部位词典类
class BodyRegions(object) :

    __verbs = {}

    def __init__(self) :

        question_file = os.path.dirname(os.path.realpath(__file__)) +\
                '/medicine_body_regions.txt'

        with  open(question_file, 'r') as fh :
            line = fh.read()
            lines = line.splitlines()
            for line in lines :
                (flag, name) = line.split()
                self.__verbs[name] = flag
        fh.close()

    def is_body_region(self, word) :

        return self.__verbs.has_key(word)

    def type_body_region(self, word) :
        if self.__verbs.has_key(word) :
            return self.__verbs[word]
        else :
            return None
