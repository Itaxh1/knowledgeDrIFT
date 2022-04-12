import json
import urllib.request
import re
from spacy_langdetect import LanguageDetector
import spacy
import nltk
from nltk import tokenize

import numpy as np
import random
import string
import re
import heapq
from parse import parseeng
from textprocessing import txtclean
from scrape import scraping



#__________________________________KNOWLEDGE DRIFT____________________________________________

def knowledgealgo(txtc):
    corpus = nltk.sent_tokenize(txtc)
    for i in range(len(corpus )):
        corpus [i] = corpus [i].lower()
        corpus [i] = re.sub(r'\W',' ',corpus [i])
        corpus [i] = re.sub(r'\s+',' ',corpus [i])
    wordfreq = {}
    for sentence in corpus:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                 wordfreq[token] += 1
    most_freq = heapq.nlargest(200, wordfreq, key=wordfreq.get)
    sentence_vectors = []
    for sentence in corpus:
        sentence_tokens = nltk.word_tokenize(sentence)
        sent_vec = []
        for token in most_freq:
            if token in sentence_tokens:
                sent_vec.append(1)
            else:
                sent_vec.append(0)
        sentence_vectors.append(sent_vec)
    sentence_vectors = np.asarray(sentence_vectors)
    l=[]
    for i in most_freq:
        if(len(i)>4):
            l.append(i)
    #count3 = 0
    tempstr1 = ''
    txtc = txtc.split('\n')
    count5=0
    for i in txtc:
        clean = False
        for word in l:
            if word in i:
                clean = True
        if clean == True:
            tempstr1 += i + '\n\n' 
            count5 += 1
            #count3 += 1
    
    return tempstr1
        
def jsonfilew(data):
    tokenize.sent_tokenize(data)
    json_string = json.dumps(data)
    json_string= [line.rstrip() for line in data.split('.') if line]
    key= []
    for i in range (0,len(json_string)):
        key.append(i)    
    res = dict(zip(key, json_string))
    print(res)
    with open("features.json", "w") as outfile:
        outfile.write(json.dumps(res))
    

def main(s):
    s.split('=')[1]
    s= main()
    a = scraping(s)
    b = parseeng(a)
    txtc = txtclean(b)
    data= knowledgealgo(txtc)  
    jsonfilew(data)

