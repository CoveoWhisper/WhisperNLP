import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import math

# retrieve text of all documents
whole_text = ''
documents_dict = {}
for i in range(1,11):
    bin_file = open('parsed_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    name = str(i)
    documents_dict[name] = text
    whole_text += text

# ************************************************** create model ************************************************
count_vectorizer = CountVectorizer()
data_frame = pd.DataFrame(count_vectorizer.fit_transform(documents_dict.values()).toarray(), columns=count_vectorizer.get_feature_names(), index=None)
data_frame.to_csv('../AI_models/word_count.csv', encoding='utf-8', index=False)
print(count_vectorizer.get_feature_names())

# ************************************************* apply model to whole text *************************************

result = count_vectorizer.transform([whole_text])

feature_names = count_vectorizer.get_feature_names()
scores = []
for col in result.nonzero()[1]:
    new_score = (feature_names[col], math.ceil(result[0,col]*1000)/1000)
    scores.append(new_score)

print(sorted(scores, key=lambda x:x[1], reverse=True))

# ************************************ store word count of whole text **********************************************
file_name = '../AI_models/word_count_model.bin'
binFile = open(file_name, 'wb')
binModel = pickle.dump(result, binFile)
binFile.close()