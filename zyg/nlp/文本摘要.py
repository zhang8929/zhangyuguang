#!/user/bin/python
# coding:utf-8

import nltk
import numpy
import jieba
import codecs
import os

class SummaryTxt:
    def __init__(self,stopwordspath):
        # 单词数量
        self.N = 100
        # 单词间的距离
        self.CLUSTER_THRESHOLD = 5
        # 返回的top n句子
        self.TOP_SENTENCES = 1
        self.stopwrods = {}
        #加载停用词
        if os.path.exists(stopwordspath):
            stoplist = [line.strip() for line in codecs.open(stopwordspath, 'r', encoding='utf8').readlines()]
            self.stopwrods = {}.fromkeys(stoplist)


    def _split_sentences(self,texts):
        '''
        把texts拆分成单个句子，保存在列表里面，以（.!?。！？）这些标点作为拆分的意见，
        :param texts: 文本信息
        :return:
        '''
        splitstr = '.!?。！？'.decode('utf8')
        start = 0
        index = 0  # 每个字符的位置
        sentences = []
        for text in texts:
            if text in splitstr:  # 检查标点符号下一个字符是否还是标点
                sentences.append(texts[start:index + 1])  # 当前标点符号位置
                start = index + 1  # start标记到下一句的开头
            index += 1
        if start < len(texts):
            sentences.append(texts[start:])  # 这是为了处理文本末尾没有标

        return sentences

    def _score_sentences(self,sentences, topn_words):
        '''
        利用前N个关键字给句子打分
        :param sentences: 句子列表
        :param topn_words: 关键字列表
        :return:
        '''
        scores = []
        sentence_idx = -1
        for s in [list(jieba.cut(s)) for s in sentences]:
            sentence_idx += 1
            word_idx = []
            for w in topn_words:
                try:
                    word_idx.append(s.index(w))  # 关键词出现在该句子中的索引位置
                except ValueError:  # w不在句子中
                    pass
            word_idx.sort()
            if len(word_idx) == 0:
                continue
            # 对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
            clusters = []
            cluster = [word_idx[0]]
            i = 1
            while i < len(word_idx):
                if word_idx[i] - word_idx[i - 1] < self.CLUSTER_THRESHOLD:
                    cluster.append(word_idx[i])
                else:
                    clusters.append(cluster[:])
                    cluster = [word_idx[i]]
                i += 1
            clusters.append(cluster)
            # 对每个族打分，每个族类的最大分数是对句子的打分
            max_cluster_score = 0
            for c in clusters:
                significant_words_in_cluster = len(c)
                total_words_in_cluster = c[-1] - c[0] + 1
                score = 1.0 * significant_words_in_cluster * significant_words_in_cluster / total_words_in_cluster
                if score > max_cluster_score:
                    max_cluster_score = score
            scores.append((sentence_idx, max_cluster_score))
        return scores

    def summaryScoredtxt(self,text):
        # 将文章分成句子
        sentences = self._split_sentences(text)

        # 生成分词
        words = [w for sentence in sentences for w in jieba.cut(sentence) if w not in self.stopwrods if
                 len(w) > 1 and w != '\t']
        # words = []
        # for sentence in sentences:
        #     for w in jieba.cut(sentence):
        #         if w not in stopwords and len(w) > 1 and w != '\t':
        #             words.append(w)

        # 统计词频
        wordfre = nltk.FreqDist(words)

        # 获取词频最高的前N个词
        topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:self.N]

        # 根据最高的n个关键词，给句子打分
        scored_sentences = self._score_sentences(sentences, topn_words)

        # 利用均值和标准差过滤非重要句子
        avg = numpy.mean([s[1] for s in scored_sentences])  # 均值
        std = numpy.std([s[1] for s in scored_sentences])  # 标准差
        summarySentences = []
        for (sent_idx, score) in scored_sentences:
            if score > (avg + 0.5 * std):
                summarySentences.append(sentences[sent_idx])
                print sentences[sent_idx]
        return summarySentences

    def summaryTopNtxt(self,text):
        # 将文章分成句子
        sentences = self._split_sentences(text)

        # 根据句子列表生成分词列表
        words = [w for sentence in sentences for w in jieba.cut(sentence) if w not in self.stopwrods if
                 len(w) > 1 and w != '\t']
        # words = []
        # for sentence in sentences:
        #     for w in jieba.cut(sentence):
        #         if w not in stopwords and len(w) > 1 and w != '\t':
        #             words.append(w)

        # 统计词频
        wordfre = nltk.FreqDist(words)

        # 获取词频最高的前N个词
        topn_words = [w[0] for w in sorted(wordfre.items(), key=lambda d: d[1], reverse=True)][:self.N]

        # 根据最高的n个关键词，给句子打分
        scored_sentences = self._score_sentences(sentences, topn_words)

        top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-self.TOP_SENTENCES:]
        top_n_scored = sorted(top_n_scored, key=lambda s: s[0])
        summarySentences = []
        for (idx, score) in top_n_scored:
            print sentences[idx]
            summarySentences.append(sentences[idx])

        return sentences



if __name__=='__main__':
    obj =SummaryTxt('D:\work\Solr\solr-python\CNstopwords.txt')

    txt=u'''A型性格的人与其他种类性格的人相比更容易患痛风，这是最近研究的结果，现对A型性格的人的心理及行为特征做一解读，以利于痛风患者们不重蹈覆辙，陷入痛风反复发作的“泥潭”。

1、A型性格的人豪爽喜欢肉食，吸烟，不爱运动。易引起肥胖、高脂血症，这些都容易引发高尿酸血症。

2、A型性格的人动作敏捷，爆发式地说话、干活。

3、A型性格的人性格急躁，没有耐心，易发生与人争吵、发怒。

4、A型性格的人雄心勃勃，竞争性强，此类人的性格一般都在领导岗位，事务繁忙。

5、A型性格的人时间观念特别强，常感觉时间不够用，而且易产生压力。

6、A型性格的人情绪易波动，经常易处于愤怒与焦虑的状态之中。

以上逐条分析，每一条都是易发痛风的禁忌，所以说这就决定了患痛风的先决条件和必要条件。

因此，为了少患、不患痛风，A型性格的人要克服这些不利的因素，改变自己的不良情绪与习惯，争取不给痛风留有余地。'''
    # txt ='The information disclosed by the Film Funds Office of the State Administration of Press, Publication, Radio, Film and Television shows that, the total box office in China amounted to nearly 3 billion yuan during the first six days of the lunar year (February 8 - 13), an increase of 67% compared to the 1.797 billion yuan in the Chinese Spring Festival period in 2015, becoming the "Best Chinese Spring Festival Period in History".' \
    #      'During the Chinese Spring Festival period, "The Mermaid" contributed to a box office of 1.46 billion yuan. "The Man From Macau III" reached a box office of 680 million yuan. "The Journey to the West: The Monkey King 2" had a box office of 650 million yuan. "Kung Fu Panda 3" also had a box office of exceeding 130 million. These four blockbusters together contributed more than 95% of the total box office during the Chinese Spring Festival period.' \
    #      'There were many factors contributing to the popularity during the Chinese Spring Festival period. Apparently, the overall popular film market with good box office was driven by the emergence of a few blockbusters. In fact, apart from the appeal of the films, other factors like film ticket subsidy of online seat-selection companies, cinema channel sinking and the film-viewing heat in the middle and small cities driven by the home-returning wave were all main factors contributing to this blowout. A management of Shanghai Film Group told the 21st Century Business Herald.'
    # print txt
    print "--"
    # obj.summaryScoredtxt(txt)

    print "----"
    obj.summaryTopNtxt(txt)