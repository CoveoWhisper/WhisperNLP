import unittest
from api.model.intent import Intent


class TestIntent(unittest.TestCase):
    def test_new_intent(self):
        intent = Intent("An intent", 2)
        self.assertEqual("An intent", intent.name)
        self.assertEqual(2, intent.confidence)
