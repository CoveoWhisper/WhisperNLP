from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import heapq

LANGUAGE = 'english'


class QueryParser(object):
    def __init__(self, word_model):
        self.model = word_model

    def parseText(self, text):
        words = word_tokenize(text, language=LANGUAGE)
        regex = re.compile('[^a-zA-Z0-9]')
        words = [regex.sub('', w).lower() for w in words]
        words = [w for w in words if w]
        return words


    def parse_query(self, sentence):
        words = self.parseText(sentence)
        print('Step 1: split query in words ', words)
        stopWords = set(stopwords.words(LANGUAGE))
        words = [word for word in words if word not in stopWords]
        print('Step 2: remove stopwords ', words)
        word_tuples = [(self.model[w], w) for w in words if w in self.model]
        heapq.heapify(word_tuples)
        rarest_words = [w[1] for w in heapq.nsmallest(3, word_tuples)]
        print('Step 3: keep rarest ', rarest_words)
        return " ".join(rarest_words)
