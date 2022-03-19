import json
import urllib.request
import re
from spacy_langdetect import LanguageDetector
import spacy
import nltk
import numpy as np
import random
import string
import re
import heapq
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt


#_______________________SCRAPPING___________________________________________________
def scraping(s):
    urlData = "https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyBpQAYG2qdzDsq3WJwmBkD_4L46rkDkvQ4&textFormat=plainText&part=snippet,replies&topLevelComment&maxResults=100&videoId={}".format(s)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    decode_data=json.loads(data.decode(encoding))
    return decode_data

#______________________PARSING AND ENG________________________________________________
def parseeng(scrape):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
    text = ''
    for i in scrape['items']:
        data3=i['snippet']['topLevelComment']['snippet']['textDisplay']
        doc = nlp(data3)
        detect_language = doc._.language
        engg = detect_language['language']
        if('en' in engg):
            text = text+data3+'\n\n'
    return text

#_________________________________TEXT CLEANING AND PREPROCESSING_____________________________________________
def txtclean(text):
    keyword=['who','when','what','where','how','?','!','...','please','?','#','thanks', 'RIP', 'love', 'thank','helpful']
    text = text.split('\n\n')
    count = 0
    count1 = 0
    str4 = ''
    #print(len(text))
    for i in text:
        clean = True
        if(len(i)>5):
            count += 1
            #str4 += i + '\n\n'
            for word in keyword:
                if word in i.lower():
                    clean = False
            if clean == True:
                count1 += 1
                str4 += i + '\n\n'
    #print(count)

    #cleddprint(count1)
    return str4


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
    txtc = txtc.split('\n\n')
    for i in txtc:
        clean = False
        for word in l:
            if word in i:
                clean = True
        if clean == True:
            tempstr1 += i + '\n\n'
            #count3 += 1
    return tempstr1




#_______________________________________SENTIMENT______________________________
def sentiiment(k):
    l = []
    k = k.split('\n\n')
    for i in k:
        if (i != ''):
            text = TextBlob(i)
            senti = text.sentiment.polarity
            if(senti < 0):
                l.append([i,"negative"])
            elif(senti == 0):
                l.append([i,"neutral"])
            elif(senti > 0 and senti <=1):
                l.append([i,"positive"])
    data = pd.DataFrame(l, columns=['TEXT', 'SENTIMENT'])
    return data
   
    

        




strr = str(input('ENTER::'))
s = strr.split('=')[1]
a = scraping(s)
#print(a)
b = parseeng(a)
#print(b)
#count = 0
txtc = txtclean(b)
k = knowledgealgo(txtc)
print(k)
sen = sentiiment(k)
ax = sen['SENTIMENT'].value_counts()
print(ax)
ax.plot(kind='bar')
plt.show()
