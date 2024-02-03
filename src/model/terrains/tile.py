from abc import abstractmethod, ABC
from typing import Tuple

from model.entities.entity import Entity


class Tile(ABC):

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    def __init__(self, index: Tuple[int, int], entity: Entity = None) -> None:
        self.index = index
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

    def getIndex(self) -> Tuple[int, int]:
        return self.index

    def __repr__(self):
        return f"Tile({self.index})"

    def __str__(self):
        ...