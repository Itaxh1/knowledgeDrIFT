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
    for i in txtc:
        clean = False
        for word in l:
            if word in i:
                clean = True
        if clean == True:
            tempstr1 += i + '\n\n'
            #count3 += 1
    return tempstr1
        


def main():
    """
    strr = str(input('ENTER::'))
    s = strr.split('=')[1]
    """
    s= "M_3yoOU3-eQ"    
    return s
s= main()
a = scraping(s)
#print(a)
b = parseeng(a)
#print(b)
#count = 0
txtc = txtclean(b)
data= knowledgealgo(txtc)  

tokenize.sent_tokenize(data)
json_string = json.dumps(data)

data.split("\r\n")

data2= [line.rstrip().split() for line in data.split('.') if line]
print(data2)  

# Writing to sample.json

json_object = json.dumps(data2)

with open("sample.json", "w") as outfile:
    outfile.write(json_object)
