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
        intent = self.service.retrieve_intent(self.get_query_result('greating', 1))
        self.assertEqual('greating', intent.name)
        self.assertEqual(1, intent.confidence)

    def test_retrieve_intent_empty_name(self):
        intent = self.service.retrieve_intent(self.get_query_result('', 0))
        self.assertEqual('', intent.name)
        self.assertEqual(0, intent.confidence)

    def test_get_id_from_path(self):
        path = 'projects/whisper234/agent/entityTypes/c907d3df-b079-4de0-9d6f-6f3b7eab2c44'
        id = self.service.get_id_from_path(path)
        self.assertEqual('c907d3df-b079-4de0-9d6f-6f3b7eab2c44', id)

    def test_get_id_from_invalid_path(self):
        path = 'projects/whisper234/agent/c907d3df-b079-4de0-9d6f-6f3b7eab2c44'
        self.assertRaises(ValueError, self.service.get_id_from_path, path)
