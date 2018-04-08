import unittest
from api.dialogflow_service import DialogFlowService


class MyTestCase(unittest.TestCase):
    def test_get_id_from_path(self):
        service = DialogFlowService()
        path = 'projects/whisper234/agent/entityTypes/c907d3df-b079-4de0-9d6f-6f3b7eab2c44'
        id = service.get_id_from_path(path)
        self.assertEquals('c907d3df-b079-4de0-9d6f-6f3b7eab2c44', id)

    def test_get_id_from_invalid_path(self):
        service = DialogFlowService()
        path = 'projects/whisper234/agent/c907d3df-b079-4de0-9d6f-6f3b7eab2c44'
        self.assertRaises(ValueError, service.get_id_from_path, path)


if __name__ == '__main__':
    unittest.main()
