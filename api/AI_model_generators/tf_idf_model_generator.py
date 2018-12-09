import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from api.AI_model_generators.text_data_mining_utilities import *
import pandas as pd
import math

# retrieve text of all documents
documents_dict = {}
for i in range(1,2621):
    bin_file = open('parsed_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    name = str(i)
    documents_dict[name] = text

# **************************************************** create model ***********************************************
tfidf_vectorizer = TfidfVectorizer()
data_frame = pd.DataFrame(tfidf_vectorizer.fit_transform(documents_dict.values()).toarray(), columns=tfidf_vectorizer.get_feature_names(), index=None)
data_frame.to_csv('../AI_models/word_score.csv', encoding='utf-8', index=False)
# print(tfidf_vectorizer.get_feature_names())
# print(data_frame.shape)


# *************************************************** store model *************************************************
file_name = '../AI_models/query_model.bin'
binFile = open(file_name, 'wb')
binModel = pickle.dump(tfidf_vectorizer, binFile)
binFile.close()

# ************************************************* apply model ***************************************************
'''
# to apply model make in comment all the above

bin_file = open('../AI_models/query_model.bin', 'rb')
model = pickle.load(bin_file)
bin_file.close()

query = 'Hello, Can I push analytics to the organization?'
result = model.transform([parseText(query)])

feature_names = model.get_feature_names()
scores = []
for col in result.nonzero()[1]:
    new_score = (feature_names[col], math.ceil(result[0,col]*1000)/1000)
    scores.append(new_score)

# print(sorted(scores, key=lambda x:x[1], reverse=True))
'''