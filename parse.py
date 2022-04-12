
from spacy_langdetect import LanguageDetector
import spacy
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
