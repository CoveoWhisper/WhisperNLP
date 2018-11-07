from api.model.entity import Entity


class NLPAnalysis:
    def __init__(self):
        self.intents = []
        self.entities = []
        self.query = ""

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_entities(self, entities):
        for i, entity in entities.items():
            self.add_entity(Entity(entity))

    def add_intent(self, intent):
        self.intents.append(intent)

    def add_query(self, query):
        self.query = query
