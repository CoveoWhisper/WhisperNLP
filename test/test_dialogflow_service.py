import unittest
from api.model.NLPAnalysis import NLPAnalysis
from api.dialogflow_service import DialogFlowService
import dialogflow


class TestDialogflowService(unittest.TestCase):

    def setUp(self):
        self.service = DialogFlowService()

    def get_query_result(self, name, confidence):
        query_result = dialogflow.types.QueryResult()
        query_result.intent.display_name = name
        query_result.intent_detection_confidence = confidence
        return query_result

    def test_retrieve_intent(self):
        intent = self.service.retrieve_intent(self.get_query_result('greeting', 1))
        self.assertEqual('greeting', intent.name)
        self.assertEqual(1, intent.confidence)

    def test_retrieve_intent_empty_name(self):
        intent = self.service.retrieve_intent(self.get_query_result('', 0))
        self.assertEqual('', intent.name)
        self.assertEqual(0, intent.confidence)


if __name__ == '__main__':
    unittest.main()
