from sklearn.feature_extraction.text import TfidfVectorizer
import math

LANGUAGE = 'english'


class QueryParser(object):
    def __init__(self, query_model):
        self.model = query_model

    def parse_query(self, sentence):
        tfidf = self.model.transform([sentence])

        feature_names = self.model.get_feature_names()
        scores = []
        for col in tfidf.nonzero()[1]:
            new_score = (feature_names[col], math.ceil(tfidf[0, col] * 1000) / 1000)
            scores.append(new_score)
        print('word score :', sorted(scores, key=lambda x: x[1], reverse=True))

        return ' '.join([score[0] for score in scores])