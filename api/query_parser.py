import math
import re

from unidecode import unidecode

from api.text_data_mining import parseText, get_word_mapping

LANGUAGE = 'english'


def simplify_string(string):
    string_without_accents = unidecode(string)
    string_without_special_characters = re.sub('[\W_]+', ' ', string_without_accents)
    stripped_string = string_without_special_characters.strip()
    lowercased_string = stripped_string.lower()
    return lowercased_string


def get_words_ordered_by_descending_score(parsed_word_by_word, scores):
    word_by_parsed_word = {value: key for (key, value) in parsed_word_by_word.items()}
    query_word_score = [(word_by_parsed_word[word], score) for (word, score) in scores]
    query_word_score.extend([(word, 0) for (word, parsed_word) in parsed_word_by_word.items() if parsed_word == ''])
    query_word_score = sorted(query_word_score, key=lambda x: x[1], reverse=True)
    result = ' '.join([word for (word, score) in query_word_score])
    return result


class QueryParser(object):
    def __init__(self, query_model):
        self.model = query_model

    def parse_query(self, sentence):
        simple_sentence = simplify_string(sentence)
        parsed_word_by_word = get_word_mapping(simple_sentence)
        tfidf = self.model.transform([parseText(simple_sentence)])
        feature_names = self.model.get_feature_names()
        scores = []
        for col in tfidf.nonzero()[1]:
            new_score = (feature_names[col], math.ceil(tfidf[0, col] * 1000) / 1000)
            scores.append(new_score)
        return get_words_ordered_by_descending_score(parsed_word_by_word, scores)

