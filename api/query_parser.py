from api.text_data_mining import *
from collections import Counter

LANGUAGE = 'english'


class QueryParser(object):
    def __init__(self, word_model):
        self.model = Counter(word_model)

    def parse_query(self, sentence):
        # keep relevant words in model : this step will be removed when the model is completely optimized
        print(self.model.most_common())
        self.model = remove_rare_words(self.model, (1,2))
        self.model = remove_most_common_word(self.model)
        self.model = remove_most_common_word(self.model)
        print('Step 1: keep relevant words in model', self.model.most_common())
        bag_of_words = word_tokenize(parseText(sentence))
        print('Step 2: parse and split query in words', bag_of_words)
        word_counts = Counter({w: self.model[w] for w in bag_of_words if w in self.model})
        print('Step 3: word counts', word_counts)

        return ' '.join(word_counts)
