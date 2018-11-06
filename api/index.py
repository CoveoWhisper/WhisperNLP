from flask import Flask,jsonify, request
from api.query_parser import QueryParser
from api.NLPJSONEncoder import NLPJSONEncoder
from api.dialogflow_service import DialogFlowService
from api.logger.logger_factory import LoggerFactory
app = Flask(__name__)
app.json_encoder = NLPJSONEncoder
dialogflowservice = DialogFlowService()


@app.route('/NLP/Analyze',  methods=['POST'])
def nlp_analyze():
    content = request.get_json()
    nlp_analysis = dialogflowservice.analyse_sentence(content['sentence'])
    return jsonify(nlp_analysis)


@app.route('/NLP/Parse/Query', methods=['POST'])
def ml_parse_query():
    content = request.get_json()
    parsed_query = QueryParser.parse_query(content)
    return jsonify(parsed_query)


if __name__ == '__main__':
    LoggerFactory.get_logger(__name__).info("API started")
    app.run(host='0.0.0.0')
