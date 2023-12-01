from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self):
        self.hunger: float = 0
        self.isFed: bool = False

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    @abstractmethod
    def reproduce(self) -> None:
        ...
    
    def eat(self) -> None:
        self.hunger = 0 # diminish hunger depending on the entity eaten (?)
        
    def starvedToDeath(self) -> bool:
        return self.hunger == 100
    
    def isHungry(self) -> bool:
        return self.hunger >= 50
    
    def getType(self):
        return self.__class__
