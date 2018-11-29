from flask.json import JSONEncoder
from api.model.intent import Intent
from api.model.entity import Entity
from api.model.NLPAnalysis import NLPAnalysis


class NLPJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, NLPAnalysis):
            return {
                'intents': obj.intents,
                'entities': obj.entities,
                'parsedQuery': obj.query,
            }
        elif isinstance(obj, Intent):
            return {
                'name': obj.name,
                'confidence': obj.confidence,
            }
        elif isinstance(obj, Entity):
            return {
                'name': obj.name,
            }
        return super(NLPJSONEncoder, obj).default(obj)
