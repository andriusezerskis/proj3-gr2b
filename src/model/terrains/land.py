from abc import abstractmethod, ABC
from overrides import override
from model.case import Case
from model.entities.plant import Plant
from model.entities.human import Human
from model.entities.entity import Entity

class Land(Case):
    def __init__(self, entity: Entity=None) -> None:
        super().__init__(entity)
        
    @override
    def getPossibleEntities(self):
        return {Human, Plant}
    
    def getType(self):
        return "land"