# coding: utf-8

import os

class QuestionList(object) :

    __verbs = []
    __index = 0

    def __init__(self) :

        question_file = os.path.dirname(os.path.realpath(__file__)) +\
                '/questions.20181214.txt'

        with  open(question_file, 'r') as fh :
            line = fh.read()
            lines = line.splitlines()
            for line in lines :
                self.__verbs.append(line)
        fh.close()

        self.__index = 0

    def getQuestion(self) :

        if self.__index < len(self.__verbs) :
            q = self.__verbs[self.__index]
            self.__index += 1
            return q
        else :
            return None
