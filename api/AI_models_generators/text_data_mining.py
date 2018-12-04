from api.AI_models_generators.text_data_mining_utilities import *
from  collections import Counter
import matplotlib.pyplot as plt

COMMON_WORDS_PORTION = 0.02
RARE_WORDS_PORTION = 0.2

custom_stopwords = []
whole_text = ''
document_text = {}

for i in range(1,11):
    bin_file = open('../extractors/extracted_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    text = parseText(text)
    document_text[i] = text
    whole_text += text

word_score = Counter(whole_text.split())
print(word_score.most_common())

# ***************************************plot before removing common and rare words
counts = [score for word, score in word_score.most_common()]

ids = [x for x in range(len(counts)+1) if x]
print(ids)
plt.scatter(ids, counts, s=1)
plt.title("Visualisation des nombres d'occurrences des mots dans tous les documents")
plt.xlabel("ids des mots")
plt.ylabel("nombres d'occurrences")
# plt.show()

# ************************************************* removing common and rare words

common_words = [word for word, score in word_score.most_common(int(len(counts) * COMMON_WORDS_PORTION))]
custom_stopwords.extend(common_words)
print('common words count : ', int(len(counts) * COMMON_WORDS_PORTION))
print('common words : ',common_words)

n= int(len(counts) * RARE_WORDS_PORTION)
rare_words = [ word for word, score in word_score.most_common()[:-n-1:-1]]
custom_stopwords.extend(rare_words)
print('rare words count : ', n)
print('rare words :', rare_words)

final_word_count = {word:word_score[word] for word in word_score if word not in custom_stopwords }

document_text_cleaned = {name:remove_custom_stop_words(text, custom_stopwords) for name, text in document_text.items() }
print('whole text before cleaning : ',document_text.values())
print('whole text after cleaning : ',document_text_cleaned.values())

# *********************************************plot after removing common and rare words
counts = [score for word, score in Counter(final_word_count).most_common()]
ids = [x for x in range(len(counts)+1) if x]

plt.scatter(ids, counts, s=1)
plt.title("Visualisation des nombres d'occurrence des mots dans tous les documents")
plt.xlabel("ids des mots")
plt.ylabel("nombres d'occurrences")
# plt.show()
'''''''''
for i in range(1,11):
    file_name = 'parsed_documents/' + str(i) + '.bin'
    binFile = open(file_name, 'wb')
    text = document_text_cleaned[i]
    binModel = pickle.dump(text, binFile)
    binFile.close()'''''