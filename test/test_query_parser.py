import unittest

from api.query_parser import simplify_string, get_words_ordered_by_descending_score


class TestQueryParser(unittest.TestCase):
    def test_remove_special_characters(self):
        self.assertEqual(
            'hello i would love to eat over 9000 apples right now',
            simplify_string('héllô!I#%   ?&would.love ,to;) *)eat_^over%9000(apples/right~NOW! !')
        )

    def test_get_words_ordered_by_descending_score_with_happy_path(self):
        parsed_word_by_word = {
            'help': 'help'
        }
        scores = [
            ('help', 1)
        ]
        actual = get_words_ordered_by_descending_score(parsed_word_by_word, scores)
        expected = 'help'
        self.assertEqual(expected, actual)

    def test_get_words_ordered_by_descending_score_with_words_of_different_scores(self):
        parsed_word_by_word = {
            'Thank': 'thank',
            'help': 'help'
        }
        scores = [
            ('thank', 0.8),
            ('help', 0.5)
        ]
        actual = get_words_ordered_by_descending_score(parsed_word_by_word, scores)
        expected = 'Thank help'
        self.assertEqual(expected, actual)

    def test_get_words_ordered_by_descending_score_with_stemmed_word(self):
        parsed_word_by_word = {
            'welcome': 'welcom'
        }
        scores = [
            ('welcom', 1)
        ]
        actual = get_words_ordered_by_descending_score(parsed_word_by_word, scores)
        expected = 'welcome'
        self.assertEqual(expected, actual)

    def test_get_words_ordered_by_descending_score_with_stemmed_word_with_no_score(self):
        parsed_word_by_word = {
            'Goodbye': 'goodby'
        }
        scores = []
        actual = get_words_ordered_by_descending_score(parsed_word_by_word, scores)
        expected = ''
        self.assertEqual(expected, actual)

    def test_get_words_ordered_by_descending_score_with_parsed_word_empty(self):
        parsed_word_by_word = {
            'empty_when_parsed': '',
            'minutes': 'minut'
        }
        scores = [
            ('minut', 1)
        ]
        actual = get_words_ordered_by_descending_score(parsed_word_by_word, scores)
        expected = 'minutes empty_when_parsed'
        self.assertEqual(expected, actual)

    def test_get_words_ordered_by_descending_score_are_ordered_correctly(self):
        parsed_word_by_word = {
            'JS': 'j',
            'framework': 'framework',
            'monkey': 'monkey',
            'patch': 'patch',
            'component': 'compon',
            'methods': 'method',
            'jQuery': 'jqueri',
            'extension': 'extens'
        }
        scores = [
            ('monkey', .6),
            ('patch', .5),
            ('jqueri', .4),
            ('extens', .3),
            ('method', .2),
            ('framework', .1),
            ('compon', .05)
        ]
        actual = get_words_ordered_by_descending_score(parsed_word_by_word, scores)
        expected = 'monkey patch jQuery extension methods framework component'
        self.assertEqual(expected, actual)
