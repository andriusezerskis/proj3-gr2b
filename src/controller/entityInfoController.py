from model.entities.entity import Entity
# from view.entityInfoView import EntityInfoModel


class EntityInfoController:
    def __init__(self, entity: Entity):
        # self.model = EntityInfoModel(entity)
        pass

    def draw_entity_info(self):
        self.model.draw_entity_info()
