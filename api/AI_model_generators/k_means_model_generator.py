import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import pickle
from api.AI_model_generators.text_data_mining_utilities import parseText


# ********************************************** create model ***************************************************
# calculate tf-idf
all_documents = {}
for i in range(1, 2621):
    bin_file = open('parsed_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    name = str(i)
    all_documents[name] = text

tf_idf_vectorizer = TfidfVectorizer(analyzer="word", use_idf=True, smooth_idf=True, ngram_range=(2, 3))
tf_idf_matrix = tf_idf_vectorizer.fit_transform(all_documents.values())
print(tf_idf_matrix)

num_clusters = 10
num_seeds = 10
max_iterations = 300
labels_color_map = {
    0: '#20b2aa', 1: '#ff7373', 2: '#f9004a', 3: '#005073', 4: '#4d0404',
    5: '#c400f9', 6: '#4700f9', 7: '#f6f900', 8: '#00f91d', 9: '#da8c49'
}
pca_num_components = 2
tsne_num_components = 2

# create k-means model
clustering_model = KMeans(
    n_clusters=num_clusters,
    max_iter=max_iterations,
    precompute_distances="auto",
    n_jobs=-1
)
clustering_model_result = clustering_model.fit(tf_idf_matrix)
print('all clusters : ',clustering_model.labels_.tolist())

#************************************************* save model ********************************************************
file_name = '../AI_models/tf_idf_vectorizer.bin'
binFile = open(file_name, 'wb')
binModel = pickle.dump(tf_idf_vectorizer, binFile)
binFile.close()

file_name = '../AI_models/k_means_clustering_model.bin'
binFile = open(file_name, 'wb')
binModel = pickle.dump(clustering_model_result, binFile)
binFile.close()

#************************************************** apply model ***************************************************
'''
# to apply model make in comment all the above

bin_file = open('../AI_models/tf_idf_vectorizer.bin', 'rb')
tf_idf_vectorizer = pickle.load(bin_file)
bin_file.close()
bin_file = open('../AI_models/k_means_clustering_model.bin', 'rb')
clustering_model = pickle.load(bin_file)
bin_file.close()

pca_num_components = 2
tsne_num_components = 2
labels_color_map = {
    0: '#20b2aa', 1: '#ff7373', 2: '#f9004a', 3: '#005073', 4: '#4d0404',
    5: '#c400f9', 6: '#4700f9', 7: '#f6f900', 8: '#00f91d', 9: '#da8c49'
}


documents = {}
for i in range(1000, 1070):
    bin_file = open('../extractors/extracted_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    name = str(i)
    documents[name] = parseText(text)
    
query = 'Hello, can I push analytics to the organization?'
query = parseText(query)
predicting_data = []
predicting_data.append(query)
predicting_data.extend(documents.values())

tf_idf_matrix_test = tf_idf_vectorizer.transform(predicting_data)
labels = clustering_model.predict(tf_idf_matrix_test)
print('testing clusters : ', labels.tolist()) 

X = tf_idf_matrix_test.todense()

# reduce data with PCA and plot
reduced_data = PCA(n_components=pca_num_components).fit_transform(X)

fig, ax = plt.subplots()
for index, instance in enumerate(reduced_data):
    pca_comp_1, pca_comp_2 = reduced_data[index]
    color = labels_color_map[labels[index]]
    ax.scatter(pca_comp_1, pca_comp_2, c=color)
plt.show()

# reduce data with t-SNE and plot
embeddings = TSNE(n_components=tsne_num_components)
Y = embeddings.fit_transform(X)
plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
plt.show()
'''
