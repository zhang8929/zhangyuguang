#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class WordType(object):

    def __init__ (self) :
        pass

    def types(self, word) :

        if word in words_jibin:
            return 'nM_JB'
        else if word in words_zhengzhuang :
            return 'nM_ZZ'
        else if word in words_keshi :
            return 'nM_YP'
