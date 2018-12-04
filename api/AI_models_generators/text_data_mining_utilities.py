import pickle
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import re
from collections import Counter

LANGUAGE = 'english'

def parseText(text):
    text = lower_cases(text)
    text = remove_noise(text)
    text = remove_numbers(text)
    text = remove_punctuation(text)
    #print(text)
    text = remove_stop_words(text)
    #print("remove stop words : %s" % text)
    text = remove_chatbot_stop_words(text)
    #print("remove chatbot stop words : %s" % text)
    text = do_lemmatization(text)
    #print("Lemmatization : %s" % text)
    text = do_stemming(text)
    #print("Stemming: %s" % text)

    return text

def lower_cases(text):
    return text.lower()
def remove_noise(text):
    words = word_tokenize(text)
    noise_sub_words = ['www', '/', '<0x', '@']
    for index in range(len(words)):
       for noise_sub_word in noise_sub_words:
           if noise_sub_word in words[index]:
                words[index] = ''
    return ' '.join([word for word in words if word])
def remove_numbers(text):
    return re.sub(r'\d+', ' ', text)
def remove_punctuation(text):
    return  re.sub(r'\W+|\_', ' ', text)
def remove_stop_words(text):
    stop_words = stopwords.words(LANGUAGE)
    return ' '.join([i for i in word_tokenize(text) if i not in stop_words])
def remove_chatbot_stop_words(text):
    #fichier = open('stopwords/chatbot_stop_words.txt', 'r') # when runing text_data_mining.py
    fichier = open('AI_models_generators/stopwords/chatbot_stop_words.txt', 'r') # when runing index.py
    chatbot_stop_words = fichier.read()
    fichier.close()
    # fichier = open('stopwords/stop_words_with_personal_names.txt', 'r') # when runing text_data_mining.py
    fichier = open('AI_models_generators/stopwords/stop_words_with_personal_names.txt', 'r') # when runing index.py
    stop_words = fichier.read()
    fichier.close()
    stop_words += chatbot_stop_words
    return ' '.join([i for i in word_tokenize(text) if i not in stop_words.split()])
def remove_custom_stop_words(text, custom_stop_words):
    return ' '.join([i for i in word_tokenize(text) if i not in custom_stop_words])
def do_stemming(text):
    stemmer = SnowballStemmer(LANGUAGE)
    return ' '.join([stemmer.stem(i) for i in word_tokenize(text)])
def do_lemmatization(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(i) for i in word_tokenize(text)])

def get_word_counts(documents_dict):
    big_text = ''
    for document_name in documents_dict.keys():
        big_text += documents_dict[document_name]
    return Counter(big_text.split())
def remove_rare_words(words_count, least_counts_to_remove):
    min_count = 0
    least_counts_to_remove = (1, 2)
    for word in words_count:
        if words_count[word] in least_counts_to_remove:
            min_count += 1
    words_to_remove = words_count.most_common()[:-min_count-1:-1]
    return (words_count - Counter(dict(words_to_remove)))
def remove_most_common_word(words_count):
    most_common_word = words_count.most_common(1)
    return words_count - Counter(dict(most_common_word))
def get_word_mapping (text):
    words = {word : parseText(word) for word in text.split()}
    query_words = {word : parsed_word for (word, parsed_word) in words.items() if
                   parsed_word or word.isdigit() or word[1:].replace(".", "", 1).isdigit()}
    unique_query_words = {}
    for word, parsed_word in query_words.items():
        if parsed_word not in unique_query_words.values() or parsed_word == '':
            unique_query_words[word] = parsed_word
    return unique_query_words