#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class SemanticsNode(object):

    word = ''
    rely_id = None
    index_id = None
    tag = None
    relation = None
    parent = None
    children = []
    __ignore_word_tags = ('x', 'd')

    def __init__ (self) :
        pass


    def children_words(self, joinChildWords = False) :

        words = []

        for node in self.children :
            word = node.word
            rel  = node.relation
            tag  = node.tag

            if tag in self.__ignore_word_tags :
                word = ''

            joinedWords = node.children_words(True)
            if len(joinedWords) == 0 :
                if len(word) > 0 :
                    words.append(word)
            elif len(joinedWords) == 1 :
                strWord = word + joinedWords[0]
                if len(strWord) > 0 :
                    words.append(strWord)
            else :
                if len(word) > 0 :
                    words.append(word)
                for jWord in joinedWords :
                    if len(jWord) > 0 :
                        words.append(jWord)

        return words
