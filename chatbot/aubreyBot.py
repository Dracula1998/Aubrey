#!/usr/bin/env python
# -*- coding:utf-8-*-
# encoding=utf-8
import importlib, sys
import sys, os, random, time, re, math, pickle, jieba
import queue, socket, threading
import numpy as np
from gensim import models
from Util import sentence2Vec
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from Miscreants import MiscreantAccount, MiscreantScalping, MiscreantSimcard

question = [u'需要几个', u'明白吧', u'?', u'为何', u'请教', u'请问', u'谁能', u'谁要', u'谁想', u'谁是', u'谁的', u'谁有', u'什么', u'啥', u'哪个',
            u'哪些', u'哪家', u'哪儿', u'哪里', u'几时', u'何时', u'多少', u'怎么', u'怎的', u'怎样', u'怎么样', u'怎么着', u'如何', u'为什么', u'为啥',
            u'为毛', u'吗', u'呢', u'怎么会', u'有谁', u'会不会', u'干嘛', u'干什么', u'干吗', u'到底', u'究竟', u'难道', u'是否', u'能否', u'能不能']


# check if sentence is question or not
def isQuestion(sentence):
    for q in question:
        if sentence.find(q) != -1:
            return True
    return False


# check if sentence is meaningful or not
def isMeaningLess(sentence):
    meaningless = [u'嗯', u'en', u'嗯嗯', u'enen', u'哦', u'哦哦', u'哈哈', u'haha', u'哈哈哈', u'hao', u'好的', u'好', u'是啊', u'是的',
                   u'[美女]', u'[美食]', u'[乒乓]', u'[胜利]', u'[差劲]', u'[菜刀]', u'[乱舞]', u'[亲亲]', u'[什么]', u'[伙伴]', u'[伤心]',
                   u'[便便]', u'[偷笑]', u'[傲慢]', u'[再见]', u'[冷汗]', u'[凋谢]', u'[分手]', u'[动物]', u'[努力]', u'[勾引]', u'[发呆]',
                   u'[发怒]', u'[发抖]', u'[可怜]', u'[可爱]', u'[右哼哼]', u'[右太极]', u'[呲牙]', u'[咒骂]', u'[咖啡]', u'[嘴唇]', u'[回头]',
                   u'[坏笑]', u'[墨镜]', u'[大哭]', u'[天使]', u'[太极]', u'[太阳]', u'[奋斗]', u'[好的]', u'[委屈]', u'[害羞]', u'[尖叫]',
                   u'[尴尬]', u'[左哼哼]', u'[左太极]', u'[得意]', u'[微笑]', u'[心碎]', u'[快乐]', u'[快哭了]', u'[怄火]', u'[恶搞]', u'[悠闲]',
                   u'[惊恐]', u'[惊讶]', u'[愉快]', u'[憨笑]', u'[打击]', u'[抓狂]', u'[投降]', u'[抠鼻]', u'[抱拳]', u'[拥抱]', u'[拳头]',
                   u'[挥手]', u'[握手]', u'[撇嘴]', u'[擦汗]', u'[敲打]', u'[流汗]', u'[流泪]', u'[激动]', u'[炸弹]', u'[爱你]', u'[爱心]',
                   u'[爱情]', u'[猪头]', u'[献吻]', u'[玫瑰]', u'[瑜伽]', u'[瓢虫]', u'[生日]', u'[疑问]', u'[疯了]', u'[白眼]', u'[磕头]',
                   u'[礼物]', u'[秘密]', u'[篮球]', u'[糗大了]', u'[糟糕]', u'[蛋糕]', u'[表情]', u'[西瓜]', u'[调皮]', u'[足球]', u'[跳绳]',
                   u'[跳跳]', u'[转圈]', u'[鄙视]', u'[闪电]', u'[闭嘴]', u'[阴险]', u'[难过]', u'[飞吻]', u'[饥饿]', u'[骷髅]', u'[高兴]',
                   u'[鲜花]', u'[鼓掌]', u'[啤酒]', u'[哈欠]', u'[月亮]', u'[乱]', u'[鬼]', u'[不]', u'[亲]', u'[优]', u'[傲]', u'[饭]',
                   u'[饿]', u'[骂]', u'[刀]', u'[勾]', u'[吐]', u'[吓]', u'[吻]', u'[哀]', u'[哑]', u'[哭]', u'[唇]', u'[嘘]',
                   u'[酒]', u'[酷]', u'[囧]', u'[困]', u'[圈]', u'[坏]', u'[奇]', u'[差]', u'[弱]', u'[强]', u'[怒]', u'[怕]',
                   u'[恭]', u'[抠]', u'[拜]', u'[晕]', u'[枯]', u'[水果]', u'[汗]', u'[顶]', u'[电]', u'[爱]', u'[闲]', u'[累]',
                   u'[羞]', u'[臭]', u'[舞]', u'[色]', u'[虫]', u'[疯]', u'[赞]', u'[衰]', u'[跳]', u'[看]', u'[睡]', u'[笑]']
    for tmp in meaningless:
        if sentence == tmp:
            return True
    return False


# # get word frequency as a dict
# def getFreqDict():
#     freqDict = {}
#     N = 0.0
#     # calculate the word frequency of your corpus for training the
#     # word2vec model
#     with open("/data/tyx/zstp/chatbot/model/wiki.zh.word.txt", 'r') as f:
#         for line in f:
#
#             line = line.strip().encode('utf-8').decode('utf-8')
#
#             if len(line) > 0:
#                 line = line.split(" ")
#                 print(float(line[1]))
#                 if len(line) == 2:
#                     freqDict[line[0]] = float(line[1])
#                     N += float(line[1])
#         #print(freqDict)
#     for key, value in freqDict.items():
#         freqDict[key] = float(value) / N
#     # keep the results for future use
#     #pickle.dump(freqDict, open( "freqDict.p", "wb" ) )
#     return freqDict

def getFreqDict():
    fp = open("freqDict.p", "rb+")
    freqDict = pickle.load(fp)

    return freqDict


# get the knowledge base dialogue pairs, in the format:
# question_tokens ;; question ;; answer ;; answer_tokens
# 怎么 安全 的 养小号 ;; 怎么安全的养小号 ;; 慢慢养着呗 或者百度 ;; 慢慢 养着 呗   或者 百度
def getSentDict():
    sentDict = {}
    for line in open("../dataCollection/zhuanke8.qa.pair.txt", 'r', encoding='utf-8'):
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


# given a sentence, calculate the sentenceVec
def getSentVec(sentence):
    a = 1e-3
    embedding_size = 250
    minFreq = min(freqDict.values())
    vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
    wordList = sentence.split(" ")
    # sentence_length = len(wordList)
    sentence_length = 0
    for word in wordList:
        # word = word.decode('utf-8')
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
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below
    # resulting sentence vectors, vs = vs -u x uT x vs
    sub = np.multiply(u, vs)
    vs = np.subtract(vs, sub)
    return vs


# get similar sentences
def getSimSents(sentence):
    t1 = time.time()
    simDict = {}
    vs = getSentVec(sentence)
    if vs is None:
        return simDict
    vs = np.array(vs)
    vs = vs.reshape(1, -1)
    for i, sentence in enumerate(sentDict.keys()):
        simSent = []
        curSentVec = sentence_vecs[i]
        curSentVec = np.array(curSentVec)
        curSentVec = curSentVec.reshape(1, -1)
        try:
            sim = cosine_similarity(vs, curSentVec)[0][0]
            if sim >= 0.82:
                print(sim, sentence)
                simSent.append(sentence)
                simSent.extend(sentDict.get(sentence))
                simDict[sim] = simSent
        except Exception as e:
            return simDict
    print("SimSent = %d, Time = %.2f" % (len(simDict), time.time() - t1))
    return simDict


def getCosSimlarity2(vs1, vs2, simSent, simDict):
    try:
        sim = cosine_similarity(vs1, vs2)[0][0]
        simDict[sim] = [simSent]
    except Exception as e:
        print(e)


# make sure the answers and questions are not questions at the same time
def noQSameTime(sentence, candidateList, oriSentence):
    simDict = {}
    vs = getSentVec(sentence)
    if vs is None:
        return simDict

    vs = np.array(vs)
    vs1 = vs.reshape(1, -1)

    isQ = False
    isQ = isQuestion(oriSentence)
    # candidateList = [[ans1, ans1split],[ans2, ans2split]]
    # candidate = [ans1, ans1split]
    for candidate in candidateList:
        can = candidate[0]
        if (isQ and not isQuestion(can)) or (not isQ and isQuestion(can)):
            can2 = candidate[1]
            vs = getSentVec(can2)
            if vs is None:
                continue
            vs = np.array(vs)
            vs2 = vs.reshape(1, -1)
            getCosSimlarity2(vs1, vs2, can, simDict)

    return simDict


# simSents = [(0.9: [sentence, [ans1, ans1split],[ans2, ans2split]]), (0.8: [sentence2, [ans11, ans11split],[ans22, ans22split]])]
def getBestChoice(sentence, simSents, oriSentence):
    candidateList = []
    simDict = {}
    for simSent in simSents:
        # simSent = (0.9: [sentence, [ans1, ans1split],[ans2, ans2split]])
        sim = simSent[0]
        # candidates = [[ans1, ans1split],[ans2, ans2split]]
        candidates = simSent[1][1:]
        if sim > 0.9:
            simDict[sim] = candidates
        candidateList.extend(candidates)
    # candidates = [我这几天很多平台试过啊 都很难出, 我 这 几天 很 多 平台 试过 啊   都 很 难出]
    # candidateList = [[我这几天很多平台试过啊 都很难出, 我 这 几天 很 多 平台 试过 啊   都 很 难出], [实付多少钱, 实付 多少钱]]
    # 如果存在基本一样的问题，则直接返回原问题的答案列表
    if len(simDict) > 0:
        print("ChatEngine:\texist original answers")
        tmpDict = {}
        for sim, simSentList in simDict.items():
            tmp = []
            for simSent in simSentList:
                tmp.append(simSent[0])
            tmpDict[sim] = tmp
        return tmpDict

    simDict = noQSameTime(sentence, candidateList, oriSentence)
    return simDict


def chatThread(miscreant, sentence):
    print(sentence)
    sentence = sentence.strip()
    oriSentence = sentence
    if sentence == "ENDEND":
        bestAnswer = "ENDEND"
    elif len(sentence) == 0 or isMeaningLess(sentence) or miscreant.firstChat or not isQuestion(sentence):
        print("ChatEngine process:\tMeaningless or not question")
        bestAnswer = miscreant.getAnswer(sentence)
    else:
        print("ChatEngine process:\tHuman ask a question")
        senlist = list(jieba.cut(sentence, cut_all=False))
        sentence = " ".join(senlist)
        simSents = getSimSents(sentence)
        simSents = sorted(simSents.items(), key=lambda d: d[0], reverse=True)
        if len(simSents) == 0:
            print("ChatEngine process:\tNo sim question")
            bestAnswer = miscreant.getAnswer(sentence)
        else:
            bestAnswerDict = {}
            bestAnswerDict = getBestChoice(sentence, simSents, oriSentence)
            bestAnswerDict = sorted(bestAnswerDict.items(), key=lambda d: d[0], reverse=True)
            if len(bestAnswerDict) == 0:
                print("ChatEngine process:\tHave sim question, but no best answer")
                bestAnswer = miscreant.getAnswer(sentence)
            else:
                print("ChatEngine process:\tHave best answer")
                try:
                    bestAnswer = bestAnswerDict[0][1][0]
                except:
                    print("ChatEngine process:\tError")
                    bestAnswer = miscreant.getAnswer(sentence)
    print("ChatEngine response:\t" + bestAnswer)
    miscreant.bestAnswer = bestAnswer
    ResponseQueue.put(miscreant)


def flushMiscreatDict(MiscreantDict):
    for senderQQ, senderInfo in MiscreantDict.items():
        MiscreantDict[senderQQ] = [senderInfo[0]]


# using a queue to record all the msgs from diff miscreants
def rspAll(conn):
    rspList = []
    while not ResponseQueue.empty():
        miscreant = ResponseQueue.get()
        bestAnswer = miscreant.bestAnswer
        if bestAnswer.startswith("ENDEND"):
            EndMiscreats.append(miscreant.senderQQ)
            rspList.append(miscreant.senderQQ + " - " + bestAnswer.split("ENDEND")[1])
        else:
            rspList.append(miscreant.senderQQ + " - " + bestAnswer)
    print(" ;; ".join(rspList))
    conn.send(" ;; ".join(rspList).encode('utf-8'))


# pre-processing the messages pass from the coolq bot
# seperate the messages of diff roles
def processMsg(sentence):
    for sent in sentence.split(" ;; "):
        senderQQ, senderName, msgText = sent.split(" - ")
        role = roleDict.get(senderQQ, None)
        if not role: continue
        if senderQQ not in MiscreantDict:
            miscreant = MiscreantAccount()
            if role == "account":
                miscreant = MiscreantAccount()
            elif role == "scalping":
                miscreant = MiscreantScalping()
            elif role == "simcard":
                miscreant = MiscreantSimcard()
            miscreant.senderQQ, miscreant.senderName = senderQQ, senderName
            MiscreantDict[senderQQ] = [miscreant, msgText]
        else:
            senderInfo = MiscreantDict.get(senderQQ)
            miscreant, length = senderInfo[0], len(senderInfo)
            if length > 1:
                msg = senderInfo[1]
                msg += ", " + msgText
                MiscreantDict[senderQQ] = [miscreant, msg]
            elif length == 1:
                MiscreantDict[senderQQ] = [miscreant, msgText]


def chatEngine():
    while 1:
        # use socket to communicate with coolq bot, to get the IM msgs
        print('ChatEngine is listening ...')
        HOST, PORT = 'localhost', 50007
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(1)
        conn, addr = sock.accept()
        print('ChatEngine connected by', addr)

        while True:
            try:
                print('ChatEngine connected by', addr)
                sentences = conn.recv(1024).decode('utf-8')
                print('ChatEngine Received:\t', sentences)
                processMsg(sentences)
                miscreantList = []
                for senderQQ, miscreantInfo in MiscreantDict.items():
                    if len(miscreantInfo) == 1:
                        continue
                    miscreant, msgText = miscreantInfo
                    if senderQQ in EndMiscreats:
                        print("ChatEngine end conversation")
                        msgText = "ENDEND"
                    miscreantList.append(threading.Thread(target=chatThread, args=(miscreant, msgText)))
                    print(miscreantList)

                flushMiscreatDict(MiscreantDict)
                for thread in miscreantList:
                    thread.start()
                for thread in miscreantList:
                    thread.join()

                rspAll(conn)
            except Exception as e:
                print("connection reset")
                conn.close()
                sock.close()
                break


# get the criminal's ID and role into a dict
def readRoles():
    dic = {}
    for line in open("../resources/roles.txt"):
        senderQQ = line.split(",")[0]
        role = line.split(",")[1]
        dic[senderQQ] = role
    return dic


importlib.reload(sys)
# sys.setdefaultencoding("utf-8")

jieba.set_dictionary('../resources/dict.txt')
stopwords = [line.strip() for line in open('../resources/stopwords.txt', encoding='utf-8').readlines()]
endingwords = [line.strip() for line in open('../resources/endingwords.txt', encoding='utf-8').readlines()]
model = models.Word2Vec.load('model/wiki_corpus.model')
freqDict = getFreqDict()
sentDict = getSentDict()
# print(freqDict)
sentence_vecs, pca = sentence2Vec(model, sentDict.keys(), freqDict)

MiscreantDict = {}
ResponseQueue = queue.Queue()
EndMiscreats = []
roleDict = readRoles()
chatEngine()
