from sklearn.feature_extraction.text import TfidfVectorizer
import math
from api.AI_model_generators.text_data_mining_utilities import parseText, get_word_mapping

LANGUAGE = 'english'


class QueryParser(object):
    def __init__(self, query_model):
        self.model = query_model

    def parse_query(self, sentence):
        parsed_word_by_word = get_word_mapping(sentence)

        tfidf = self.model.transform([parseText(sentence)])

        feature_names = self.model.get_feature_names()
        scores = []
        for col in tfidf.nonzero()[1]:
            new_score = (feature_names[col], math.ceil(tfidf[0, col] * 1000) / 1000)
            scores.append(new_score)

        word_by_parsed_word = {value: key for (key, value) in parsed_word_by_word.items()}

        # if a word have multiple parsed_words so keep 1 score
        scores = [score for score in scores if score[0] in  word_by_parsed_word.keys()]

        query_word_score = [(word_by_parsed_word[word], score) for (word, score) in scores]
        query_word_score.extend([(word,0) for (word, parsed_word) in parsed_word_by_word.items() if parsed_word == ''])
        query_word_score = sorted(query_word_score, key=lambda x: x[1], reverse=True)

        return ' '.join([word for (word, score) in query_word_score])