from abc import abstractmethod, ABC
from model.entities.entity import Entity


class Tile(ABC):

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    def __init__(self, index: tuple, entity: Entity = None) -> None:
        self.index = index
        self.entity = entity
        
    # @abstractmethod
    def step(self):
        pass
    
    @abstractmethod
    def getPossibleEntities(self):
        pass
        
    def getEntity(self):
        return self.entity
    
    def addEntity(self, entity):
        if not self.entity:
            self.entity = entity
        
    def removeEntity(self):
        if self.entity:
            self.entity = None