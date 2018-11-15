import os
import uuid
import dialogflow
from api.model.intent import Intent
from api.config import config
from api.model.NLPAnalysis import NLPAnalysis

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__),
                                                            config.get('dialogflow_secret'))


class DialogFlowService:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.project_id = config.get('project_id')
        self.parent = 'projects/{}/agent'.format(self.project_id)

    def analyse_sentence(self, sentence):
        nlp_analysis = NLPAnalysis()
        query_result = self.detect_intent(sentence)
        nlp_analysis.add_intent(self.retrieve_intent(query_result))
        nlp_analysis.add_entities(query_result.parameters)
        return nlp_analysis

    def detect_intent(self, sentence):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.project_id, self.session_id)
        text_input = dialogflow.types.TextInput(text=sentence, language_code=config.get('language'))
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result

    def retrieve_intent(self, query_result):
        return Intent(query_result.intent.display_name, query_result.intent_detection_confidence)
