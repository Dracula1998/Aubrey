#!/usr/bin/env python
# -*- coding:utf-8-*-
# encoding=utf-
import importlib,sys
from gensim import models
from collections import Counter, defaultdict
#from Util import isQuestion, isEndingWord
importlib.reload(sys)
#sys.setdefaultencoding("utf-8")
model = models.Word2Vec.load('/data/ganbin/zstp/chatbot/model/wiki_corpus.model')

#endingwords = [line.strip().decode('utf-8') for line in open('D:/关系图谱/resources/endingwords.txt').readlines()]
endingwords = [line.strip() for line in open('/data/ganbin/zstp/resources/endingwords.txt', encoding='utf-8').readlines()]

def isEndingWord(msg):
    for word in endingwords:
        if msg == word:
            return True
    if len(msg.decode("utf8")) <= 2:
        return True
    return False

question = [u'需要几个', u'明白吧', u'?', u'为何', u'请教', u'请问', u'谁能', u'谁要',u'谁想',u'谁是',u'谁的',u'谁有',u'什么',u'啥',u'哪个',u'哪些',u'哪家',u'哪儿',u'哪里',u'几时',u'何时',u'多少',u'怎么',u'怎的',u'怎样',u'怎么样',u'怎么着',u'如何',u'为什么',u'为啥',u'为毛',u'吗',u'呢',u'怎么会',u'有谁',u'会不会',u'干嘛',u'干什么',u'干吗',u'到底',u'究竟',u'难道', u'是否', u'能否', u'能不能']
# check if sentence is question or not
def isQuestion(sentence):
    for q in question:
        if sentence.find(q) != -1:
            return True
    return False

def isEndingWord(msg):
    for word in endingwords:
        if msg == word:
            return True
    if len(msg.encode('utf-8').decode("utf8")) <= 2:
        return True
    return False

# SP nearest neighbor
def getDist(msg, Clusters, ClustNum):
    Dist = 100.0
    n = len(Clusters[ClustNum])
    for index, msgList in enumerate(Clusters[ClustNum],1):
        dist = model.wmdistance(msg, msgList[1])
        if index <= 6:
            Dist = min(dist, Dist)
        else:
            break
    return float(Dist)


def getDialogs(cluster,pairs):
    length = len(cluster)
    i = 0
    while i < length - 1:
        msg1 = cluster[i][1]
        msg2 = cluster[i+1][1]
        question1 = isQuestion(msg1.split(u" ")[0])
        question2 = isQuestion(msg2.split(u" ")[0])
        if msg1.split(u" ")[-1] != "EOFEOF" and not question1 or not question2 :
            pairs.write(msg1.strip(" EOFEOF") + " ;; " + msg2.strip(" EOFEOF") + "\n")
        i += 1
        if msg2.split(u" ")[-1] == "EOFEOF":
            i += 1

        
def singlePass(msgList):
    Clusters = []
    if msgList is None:
        return Clusters

    for index, msg in enumerate(msgList):
        Matched = 0
        error = False
        if len(Clusters) == 0:
            Clusters.append([(index, msg)])
            continue

        for ClustNum in reversed(range(len(Clusters))):
            index2 = Clusters[ClustNum][0][0]
            index3 = Clusters[ClustNum][-1][0]
            if index - index2 <= 6 or index - index3 <= 6:
                Dist = getDist(msg, Clusters, ClustNum)
                if Dist == float('inf') or Dist == float('nan'):
                    error = True
                    break
                if Dist < 1.1 or Dist == float('100.0') or isEndingWord(msg):
                    if Dist == float('100.0') or isEndingWord(msg):
                        msg += " EOFEOF"
                    Clusters[ClustNum].append((index, msg))
                    Matched = 1
                    break
                elif len(Clusters[ClustNum]) > 1:
                    Dist0 = model.wmdistance(msg, Clusters[ClustNum][0][1])
                    Dist1 = model.wmdistance(msg, Clusters[ClustNum][-1][1])
                    Dist = min(Dist0, Dist1)
                    if Dist < 1.21 and (index - index2 <= 2 or index - index3 <= 2):
                        Clusters[ClustNum].append((index, msg))
                        Matched = 1
                        break
        if Matched ==0 and not error:
            Clusters.append([(index, msg)])

    return Clusters

def mergeTwoList(list1, list2):
    len1 = len(list1)
    len2 = len(list2)
    tmp, i, j = [], 0, 0
    while i < len1 and j < len2:
        if list1[i][0] < list2[j][0]:
            tmp.append(list1[i])
            i += 1
        else:
            tmp.append(list2[j])
            j += 1
    if i == len1:
        tmp.extend(list2[j:])
    else:
        tmp.extend(list1[i:])
    return tmp


# get dialog pairs from forum QA data
def getDialogPairs():
    model.init_sims(replace=True)
    pairs = open("/data/ganbin/zstp/dataCollection/zhuanke8.qa.pair.txt", 'w')
    filePath = "/data/ganbin/zstp/dataCollection/zuanke8.qa.txt"
    # your_forumQA.txt in the format:
    # postID;:;title;:;post1;:;post2;:;post3;:;post4
    for line in open(filePath, 'r'):
        corpus = line.strip().split(";:;")[1:]
        clusters = singlePass(corpus)
        if len(clusters) == 0:
            continue
        clusters2 = []
        length = len(clusters)
        for i in range(length):
            if clusters2 == []:
                clusters2.append(clusters[i])
            else:
                size = len(clusters2)
                if clusters2[size-1][0][0] < clusters[i][0][0] < clusters2[size-1][-1][0] and clusters2[size-1][0][0] < clusters[i][-1][0] < clusters2[size-1][-1][0]:
                    tmp = mergeTwoList(clusters2[size-1], clusters[i])
                    del clusters2[-1]
                    clusters2.append(tmp)
                else:
                    clusters2.append(clusters[i])
        
        for cluster2 in clusters2:
            if len(cluster2) == 1:
                continue
            getDialogs(cluster2, pairs)

getDialogPairs()