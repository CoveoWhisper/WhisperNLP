import requests
import pickle
from api.extractors.factory import ExtractorFactory


URL = 'https://platform.cloud.coveo.com/rest/search/v2/'
HEADERS = {'Authorization': 'Bearer xx50034238-5a30-4808-98d3-4ef3dc9ec7cc'}
NUMBER_OF_RESULTS_PER_QUERY = 1000
ATTRIBUTES_LIST = ['title', 'tags', 'concepts', 'documenttype', 'sourcetype', 'source', 'collection', 'filetype', 'sitename']
LANGUAGE = 'english'
RAW_LANGUAGE = 'English'

#****************************************Extract texts from documents*********************************************

data = {'numberOfResults': str(NUMBER_OF_RESULTS_PER_QUERY), 'sortCriteria': '@rowid ascending', 'cq': ''}
smallerId = 0
total = 0
factory = ExtractorFactory()
text = []
text_dictionary = {}
i=0
counter = 0
while i<1:
    data['cq'] = '@rowid>' + str(smallerId)
    response = requests.post(URL, headers=HEADERS, data=data).json()

    if response["totalCount"] == 0:
        break

    smallerId = response['results'][-1]['raw']['rowid']
    total += len(response['results'])

    for result in response['results']:
        if 'language' not in result['raw'] or RAW_LANGUAGE not in result['raw']['language']:
            continue

        uniqueID = result['UniqueId']
        url = 'https://cloudplatform.coveo.com/rest/search/v2/html?uniqueId=' + uniqueID

        extractor = factory.fromFilePath(url, 'html', HEADERS)
        if extractor != None:
            extractedText = extractor.extractAllText()
            if extractedText:
                counter+=1

                file_name = 'extracted_documents/' + str(counter) + '.bin'
                binFile = open(file_name, 'wb')
                binModel = pickle.dump(extractedText, binFile)
                binFile.close()
        # if i>20: # to extract 20 files
          #  break
        # i+=1
