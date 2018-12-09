import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import matplotlib.pyplot as plt

# retrieve text of all documents
whole_text = ''
documents_dict = {}
for i in range(1,2621):
    bin_file = open('parsed_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    name = str(i)
    documents_dict[name] = text
    whole_text += text

# ************************************************** create Count Vectorizer model ************************************************
count_vectorizer = CountVectorizer()
data_frame1 = pd.DataFrame(count_vectorizer.fit_transform(documents_dict.values()).toarray(), columns=count_vectorizer.get_feature_names(), index=None)
#data_frame.to_csv('../AI_models/count_vectorizer.csv', encoding='utf-8', index=False)
# print(count_vectorizer.get_feature_names())
# print(data_frame1.shape)

# ************************************************* save Count Vectorizer model ***********************************
file_name = '../AI_models/count_vectorizer_model.bin'
binFile = open(file_name, 'wb')
binModel = pickle.dump(count_vectorizer, binFile)
binFile.close()

# ************************************************* apply Count Vectorizer model to whole text *************************************
''''
# to apply model make in comment all the above
bin_file = open('../AI_models/count_vectorizer_model.bin', 'rb')
count_vectorizer_model = pickle.load(bin_file)
bin_file.close()

result = count_vectorizer_model.transform([whole_text])

feature_names = count_vectorizer_model.get_feature_names()
scores = []
for col in result.nonzero()[1]:
    new_score = (feature_names[col], result[0,col])
    scores.append(new_score)
scores = sorted(scores, key=lambda x:x[1], reverse=True)

# ************************************ store word count of whole text **********************************************
file_name = '../AI_models/word_count.bin'
binFile = open(file_name, 'wb')
binModel = pickle.dump(result, binFile)
binFile.close()
# ***************************************** plot word count ********************************************************
counts = [score[1] for score in scores]
ids = [x for x in range(len(counts)+1) if x]
plt.scatter(ids, counts, s=1)
plt.title("Visualisation des nombres d'occurrences des mots dans tous les documents")
plt.xlabel("ids des mots")
plt.ylabel("nombres d'occurrences")
plt.show()
'''