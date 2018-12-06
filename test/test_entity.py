import unittest
from api.model.entity import Entity


class TestEntity(unittest.TestCase):

    def test_new_intent(self):
        intent = Entity("An entity")
        self.assertEqual("An entity", intent.name)
