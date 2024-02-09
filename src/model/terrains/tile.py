from abc import abstractmethod, ABC

from model.entities.entity import Entity

from utils import Point


class Tile(ABC):

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    def __init__(self, pos: Point, height: float, entity: Entity = None) -> None:
        self.pos = pos
        self.height = height
        self.entity = entity
        
    # @abstractmethod
    def step(self):
        pass
        
    def getEntity(self) -> Entity | None:
        return self.entity

    def hasEntity(self) -> bool:
        return self.entity is not None
    
    def addEntity(self, entity) -> None:
        if not self.entity:
            self.entity = entity
        
    def removeEntity(self) -> None:
        if self.entity:
            self.entity = None

    def getPos(self) -> Point:
        return self.pos

    def __repr__(self):
        return f"Tile({self.pos})"

    def __str__(self):
        ...