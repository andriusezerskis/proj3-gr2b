from abc import abstractmethod, ABC
from overrides import override
from case import Case
from entities.plant import Plant
from entities.human import Human
from entities.entity import Entity

class Land(Case):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)
        
    @override
    def getPossibleEntities(self):
        return {Human, Plant}
    
    def getType(self):
        return "land"