from abc import abstractmethod, ABC
from overrides import override
from case import Case
from entities.plant import Plant
from entities.human import Human

class Land(Case):
    def __init__(self, entityList) -> None:
        super().__init__(entityList)
        
    @override
    def getPossibleEntities(self):
        return {Human(), Plant()}
    
    def getType(self):
        return "land"