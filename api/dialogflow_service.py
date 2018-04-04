import os
import uuid
import dialogflow
from api.model.intent import Intent
from api.config import config
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get('dialogflow_secret')


class DialogFlowService:
    LANGUAGE_CODE = 'EN'

    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.project_id = config.get('project_id')
        self.parent = 'projects/{}/agent'.format(self.project_id)

    def detect_intent(self, text):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.project_id, self.session_id)
        text_input = dialogflow.types.TextInput(text=text, language_code=config.get('language'))
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return Intent(response.query_result.intent.display_name, response.query_result.intent_detection_confidence)

    def add_entity_type(self, name):
        entity_types_client = dialogflow.EntityTypesClient()

        parent = entity_types_client.project_agent_path(self.project_id)
        entity_type = dialogflow.types.EntityType(display_name=name, kind=dialogflow.enums.EntityType.Kind.KIND_LIST)

        entity_types_client.create_entity_type(parent, entity_type)

    def add_entity(self, entity_name, entity_value):
        entity_types_client = dialogflow.EntityTypesClient()
        entity_type_id = self.get_entity_type_id(entity_name)
        entity_type_path = entity_types_client.entity_type_path(self.project_id, entity_type_id)

        synonyms = [entity_value]
        entity = dialogflow.types.EntityType.Entity()
        entity.value = entity_value
        entity.synonyms.extend(synonyms)

        entity_types_client.batch_create_entities(entity_type_path, [entity], DialogFlowService.LANGUAGE_CODE)

    def add_entities(self, entity_name, entity_values):
        entity_types_client = dialogflow.EntityTypesClient()
        entity_type_id = self.get_entity_type_id(entity_name)
        entity_type_path = entity_types_client.entity_type_path(self.project_id, entity_type_id)

        entity_list = []

        for value in entity_values:
            synonyms = [value]
            entity = dialogflow.types.EntityType.Entity()
            entity.value = value
            entity.synonyms.extend(synonyms)
            entity_list.append(entity)

        entity_types_client.batch_create_entities(entity_type_path, entity_list, DialogFlowService.LANGUAGE_CODE)

    def get_entities(self):
        entity_types_client = dialogflow.EntityTypesClient()
        return entity_types_client.list_entity_types(self.parent, DialogFlowService.LANGUAGE_CODE)

    def get_entity_type_id(self, entity_display_name):
        entity_types_client = dialogflow.EntityTypesClient()
        entity_types = entity_types_client.list_entity_types(self.parent, DialogFlowService.LANGUAGE_CODE)

        for entity_type in entity_types:
            if(entity_type.display_name == entity_display_name):
                return self.get_id_from_path(entity_type.name)
        raise ValueError('No entity having specified entity_display_name')

    def get_id_from_path(self, path):
        path_elements = path.split('/')
        if(len(path_elements) != 5):
            raise ValueError('Path should be of format: "/projects/projectName/agent/entityTypes/id"')
        return path_elements[-1]
