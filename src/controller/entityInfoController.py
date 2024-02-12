from model.entities.entity import Entity
from view.entityInfo import EntityInfoModel

class EntityInfoController:
    def __init__(self, entity: Entity):
        self.model = EntityInfoModel(entity)

    def draw_entity_info(self):
        self.model.draw_entity_info()
