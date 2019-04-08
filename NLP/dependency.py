#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 测试依存句法分析处理

import os, sys

from semantics.intention import IntentionParser
from database.questions import QuestionList

questions = QuestionList()
question  = questions.getQuestion()
index = 0
parser = IntentionParser()

while question and index <= 1000 :
    intent = parser.get_intent(question)
    question  = questions.getQuestion()
    index += 1
