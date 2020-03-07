#!/usr/bin/env python
# -*- coding:utf-8-*-
# encoding=utf-8
import sys
import os
from gensim import models
import jieba
import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from Util import sentence2Vec


reload(sys)
sys.setdefaultencoding("utf-8")
jieba.set_dictionary('/resources/dict.txt')
stopwords = [line.strip().decode('utf-8') for line in open('/resources/stopwords.txt').readlines()]
model = models.Word2Vec.load('your_word2vec_model.model')
question = [u'需要几个', u'明白吧', u'?', u'为何', u'请教', u'请问', u'谁能', u'谁要',u'谁想',u'谁是',u'谁的',u'谁有',u'什么',u'啥',u'哪个',u'哪些',u'哪家',u'哪儿',u'哪里',u'几时',u'何时',u'多少',u'怎么',u'怎的',u'怎样',u'怎么样',u'怎么着',u'如何',u'为什么',u'为啥',u'为毛',u'吗',u'呢',u'怎么会',u'有谁',u'会不会',u'干嘛',u'干什么',u'干吗',u'到底',u'究竟',u'难道', u'是否', u'能否', u'能不能']


def checkKeywords(msg, msgSplit, qDict, newKeywordGroups):
    flag = True
    for newGroup in newKeywordGroups:
        tmpFlag = False
        for keyword in newGroup:
            if msg.find(keyword) != -1:
                tmpFlag = True
                break
        if not tmpFlag:
            flag = False
            break
    if flag:
        for q in question:
            if msg.find(q) != -1:
                if msg not in qDict:
                    qDict[msg] = 1
                break


def getSentDict():
    sentDict = {}
    for line in open("./knowledgeBase.txt", 'r'):    
        line = line.strip() 
        if len(line) == 0:
            continue
        try:
            msg1 = line.split(" ;; ")[0]
            msg2 = line.split(" ;; ")[2:]
            if msg1 not in sentDict:
                sentDict[msg1] = [msg2]
            else:
                tmp = sentDict.get(msg1)
                tmp.append(msg2)
                sentDict[msg1] = tmp
        except Exception as e:
            print(e)
    return sentDict



def getSentVec(sentence):
    a = 1e-3
    embedding_size = 250
    minFreq = min(freqDict.values())
    vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
    wordList = sentence.split(" ")
    # sentence_length = len(wordList)
    sentence_length = 0
    for word in wordList:
        word = word.decode('utf-8')
        if word in stopwords:
            continue
        sentence_length += 1
        try:
            a_value = a / (a + freqDict.get(word, minFreq))  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, model.wv.word_vec(word)))  # vs += sif * word_vector
        except:
            pass
    if sentence_length == 0:
        return None
    vs = np.divide(vs, sentence_length)  # weighted average
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT
    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sub = np.multiply(u,vs)
    vs = np.subtract(vs, sub)
    return vs



def getSentSimlarity(sent1, sent2):
    vs1 = getSentVec(sent1)
    if vs1 is None:
        return None
    vs1 = np.array(vs1)
    vs1 = vs1.reshape(1,-1)

    vs2 = getSentVec(sent2)
    if vs2 is None:
        return None
    vs2 = np.array(vs2)
    vs2 = vs2.reshape(1, -1)

    try:
        sim = cosine_similarity(vs1, vs2)[0][0]
        return sim
    except Exception as e:
        print(e)


def extendGroups(keywordGroups):
    newKeywordGroups = []
    for group in keywordGroups:
        newGroup = {}
        for keyword in group:
            newGroup[keyword] = 1
            try:
                for i in model.most_similar(keyword):  
                    if i[1] > 0.7:
                        newGroup[i[0]] = 1
            except:
                pass
        newKeywordGroups.append(newGroup.keys())

    return newKeywordGroups


def getQuestions(keywordGroups):
    newKeywordGroups = extendGroups(keywordGroups)
    qDict = {}
    for line in open("./knowledgeBase.txt", 'r'):    
        line = line.strip() 
        msg1 = line.split(" ;; ")[1]
        msg1Split = line.split(" ;; ")[0]
        msg2 = line.split(" ;; ")[2]
        msg2Split = line.split(" ;; ")[3]
        checkKeywords(msg1, msg1Split, qDict, newKeywordGroups)
        checkKeywords(msg2, msg2Split, qDict, newKeywordGroups)

    # questions from seed conversations, asking fake account website
    list1 = [u"哪能买小号呢，提供一下链接呗"]
    for qCandidates in qDict:
        qCandidates2 = jieba.cut(qCandidates, cut_all=False)
        qCandidates2 = " ".join(list(qCandidates2))
        tmpDict = {}
        for q in list1:
            q = jieba.cut(q, cut_all=False)
            q = " ".join(list(q))
            sentSim = getSentSimlarity(q, qCandidates2)
            if sentSim != None:
                tmpDict[sentSim] = q
        tmpDict = sorted(tmpDict.items(), key=lambda d: d[0], reverse=True)
        tmp = tmpDict[0]
        if tmp[0] > 0.9:
            print(qCandidates)



freqDict = pickle.load(open( "./freqDict.p", "rb" ))
sentDict = getSentDict()
sentence_vecs, pca = sentence2Vec(model, sentDict.keys(), freqDict)
# sets of keywords, each set contains the keywords of certain topic
# for example, sets of seeds to extend for fake account website
keywordGroups = [[u'链接', u'网站', u'网址'],[u"当天号",u"实名号",u"白号",u"账号",u"账户",u"小号",u"刷单号",u"微信号",u"VX号",u"淘宝号",u"京东号",u"耐用号",u"卖家号",u"买家号",u"老号"]]
# keywordGroups = [[u'价格', u'价钱', u'钱'],[u"当天号",u"实名号",u"白号",u"账号",u"账户",u"小号",u"刷单号",u"微信号",u"VX号",u"淘宝号",u"京东号",u"耐用号",u"卖家号",u"买家号",u"老号"]]
getQuestions(keywordGroups)
