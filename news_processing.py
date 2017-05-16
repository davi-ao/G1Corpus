from __future__ import division
from nltk import word_tokenize
from nltk.book import *
import json
import nltk


def percentage(count, total):
    return 100 * count / total

stopwords = nltk.corpus.stopwords.words('portuguese')

news_file = open('news_corpus.json').read()
news_json = json.loads(news_file)

news_titles_list = [str(o['title']) for o in news_json]
news_texts_list = [str(o['text']) for o in news_json]
news_all_raw = '. '.join(news_titles_list) + '. '.join(news_texts_list)
news_tokens = word_tokenize(news_all_raw)
news_texts = nltk.Text(news_tokens)
#news_words_len = len([w for w in news_tokens if w.isalpha()])

#news_texts.collocations()
fdist = FreqDist(w.lower() for w in news_texts if w.isalpha() and w not in stopwords and len(w) > 2)
#vocabulary = fdist.keys()

#fdist.plot(50)

target_words = ['golpe', 'impeachment']

for m in target_words:
    print m + ':', fdist[m], percentage(news_texts.count(m), len(news_texts))
