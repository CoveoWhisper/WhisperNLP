from flask import Flask, jsonify, request
from api.query_parser import QueryParser
from api.NLPJSONEncoder import NLPJSONEncoder
from api.dialogflow_service import DialogFlowService
from api.logger.logger_factory import LoggerFactory

import nltk
import pickle

app = Flask(__name__)
app.json_encoder = NLPJSONEncoder
dialogflowservice = DialogFlowService()


'''
This method analyze the query received and returns intents, entities and keywords
'''
@app.route('/NLP/Analyze',  methods=['POST'])
def nlp_analyze():
    content = request.get_json()
    query = content['sentence']
    nlp_analysis = dialogflowservice.analyse_sentence(query)
    nlp_analysis.add_query(query_parser.parse_query(query.replace('?', '')))
    return jsonify(nlp_analysis)


if __name__ == '__main__':
    word_model_file = open('query_model.bin', 'rb')
    word_model = pickle.load(word_model_file)
    word_model_file.close()
    query_parser = QueryParser(word_model)
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host='0.0.0.0')
