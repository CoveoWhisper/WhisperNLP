from api.AI_models_generators.text_data_mining_utilities import *

documents_dict = {}
for i in range(1,11):
    bin_file = open('../extractors/extracted_documents/' + str(i) + '.bin', 'rb')
    text = pickle.load(bin_file)
    bin_file.close()
    text = parseText(text)

    file_name = 'parsed_documents/' + str(i) + '.bin'
    binFile = open(file_name, 'wb')
    binModel = pickle.dump(text, binFile)
    binFile.close()