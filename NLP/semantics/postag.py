#!/usr/bin/env python
# coding: utf-8

class PosTagMapping (object) :

    __mapping_ = {}

    def __init__(self) :
		self.__mapping_ = {
		'a' : 'a',
		'ad' : 'a',
		'ag' : 'g',
		'an' : 'a',
		'b' : 'b',
		'c' : 'c',
		'd' : 'd',
		'df' : 'd',
		'dg' : 'g',
		'e' : 'e',
		'eng' : 'ws',
		'f' : 'nd',
		'g' : 'g',
		'h' : 'h',
		'i' : 'i',
		'j' : 'j',
		'k' : 'k',
		'l' : 'i',
		'm' : 'm',
		'mg' : 'g',
		'mq' : 'm',
		'n' : 'n',
		'ng' : 'g',
		'nr' : 'nh',
		'nrfg' : 'n',
		'nrt' : 'n',
		'ns' : 'ns',
		'nt' : 'ni',
		'nz' : 'nz',
        'jb' : 'nz',
        'zz' : 'nz',
        'yp' : 'nz',
        'yg' : 'g',
        'ks' : 'nz',
		'o' : 'o',
		'p' : 'p',
		'q' : 'q',
		'r' : 'r',
		'rg' : 'g',
		'rr' : 'r',
		'rz' : 'r',
		's' : 'nl',
		't' : 'nt',
		'tg' : 'g',
		'u' : 'u',
		'ud' : 'u',
		'ug' : 'u',
		'uj' : 'u',
		'ul' : 'u',
		'uv' : 'u',
		'uz' : 'u',
		'v' : 'v',
		'vd' : 'v',
		'vg' : 'g',
		'vi' : 'v',
		'vn' : 'v',
		'vq' : 'v',
		'w' : 'wp',
		'x' : 'x',
		'y' : 'e',
		'z' : 'a',
		'zg' : 'a',
		}

    def jieba2LTP(self, word_name) :

        return self.__mapping_[word_name]




if __name__ == '__main__' :
    x = PosTagMapping()
    print x.jieba2LTP('uz')
