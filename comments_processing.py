from __future__ import division
from nltk import word_tokenize
from nltk.book import *
import json
import nltk


def percentage(count, total):
    return 100 * count / total

stopwords = nltk.corpus.stopwords.words('portuguese')

comments_file = open('comments_corpus.json').read()
comments_json = json.loads(comments_file)

comments_author_list = [o['autor'] for o in comments_json]
comments_text_list = [o['texto'] for o in comments_json]
comments_author_response_list = [o['autor_resposta'] for o in comments_json if 'autor_resposta' in o]
comments_text_respose_list = [o['texto_resposta'] for o in comments_json if 'texto_resposta' in o]
comments_all_raw = '. '.join(comments_author_list) + '. '.join(comments_text_list) + '. '.join(comments_author_response_list) + '. '.join(comments_text_respose_list)
comments_texts_raw = '. '.join(comments_text_list) + '. '.join(comments_text_respose_list)
comments_tokens = word_tokenize(comments_all_raw)
comments_texts_tokens = word_tokenize(comments_texts_raw)
comments_text = nltk.Text(comments_tokens)
comments_texts_text = nltk.Text(comments_texts_tokens)
#comments_words_len = len([w for w in comments_tokens if w.isalpha()])

#comments_texts.collocations()

fdist = FreqDist(w.lower() for w in comments_text if w.isalpha() and w not in stopwords and len(w) > 2)
#fdist = FreqDist(w.lower() for w in comments_texts_text if w.isalpha() and w not in stopwords and len(w) > 2)
#fdist = FreqDist(w.lower() for w in comments_texts_text if w.isalpha() and w not in stopwords and len(w) > 3)
#fdist = FreqDist(w.lower() for w in comments_texts_text if w.isalpha() and w not in stopwords and len(w) > 4)
#vocabulary = fdist.keys()

#fdist.plot(50)

target_words = ['golpe', 'impeachment']

for m in target_words:
    print m + ':', fdist[m], percentage(comments_texts_text.count(m), len(comments_texts_text))
