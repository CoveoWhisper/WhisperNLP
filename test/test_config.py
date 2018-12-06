import unittest
from nose.tools import raises
from api.config import Config
import os


class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config(os.path.dirname(__file__))

    def test_get_dialogflow_secret_success(self):
        self.assertEqual('file.json', self.config.get('dialogflow_secret'))

    def test_get_project_id_success(self):
        self.assertEqual('whisperproject', self.config.get('project_id'))

    def test_get_language_success(self):
        self.assertEqual('en-US', self.config.get('language'))

    @raises(AttributeError)
    def test_invalid_config_key(self):
        self.assertRaises(AttributeError, self.config.get('key_invalid'))
