#!/usr/bin/env python
# -*- coding:utf-8-*-
# encoding=utf-8
import re
import numpy as np
from sklearn.decomposition import PCA
#endingwords = [line.strip().decode('utf-8') for line in open('D:/关系图谱/resources/endingwords.txt').readlines()]
endingwords = [line.strip() for line in open('../resources/endingwords.txt', encoding='utf-8').readlines()]

def isEndingWord(msg):
    for word in endingwords:
        if msg == word:
            return True
    if len(msg.decode("utf8")) <= 2:
        return True
    return False

    
def isStoreLink(sentence):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sentence)
    if len(urls) != 0:
        return True
    return False


def isNegative(sentence):
    negatives = [u'不知道', u'不清楚', u'没有', u'木有', u'没']
    for n in negatives:
        if sentence.find(n) != -1:
            return True
    return False


stopwords = [line.strip() for line in open('../resources/stopwords.txt',encoding = 'utf-8').readlines()]
embedding_size = 250
a = 1e-3
def get_word_frequency(word_text):
    return 1.0


punctuations = ['·', '~', ' ','!','@','#','$','%','^','&','*','(',')','_','+','-','=','[',']','{','}',':',';','\'','"',',','.','/','<','>','?','|','\\','！','￥','……','（','）','——','【','】','：','；','”','‘','，','《','。','》','？','、','、']

def removePunct(answer):
    for pun in punctuations:
        answer = answer.replace(pun, " ")
    return answer.strip()


def sentence2Vec(model, sentence_list, freqDict):
    minFreq = min(freqDict.values())
    sentence_set = []
    for sentence in sentence_list:    
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        wordList = sentence.split(" ")
        # sentence_length = len(wordList)
        sentence_length = 0
        for word in wordList:
            word = word.encode('utf-8').decode('utf-8')
            if word in stopwords:
                continue
            sentence_length += 1
            try:
                a_value = a / (a + freqDict.get(word, minFreq))  # smooth inverse frequency, SIF
                vs = np.add(vs, np.multiply(a_value, model.wv.word_vec(word)))  # vs += sif * word_vector
            except:
                pass
        vs = np.divide(vs, sentence_length)  # weighted average
        vs = np.nan_to_num(vs)
        sentence_set.append(vs)
    # calculate PCA of this sentence set
    pca = PCA(n_components=embedding_size)
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT
    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u,vs)
        sentence_vecs.append(np.subtract(vs, sub))
    return sentence_vecs, pca