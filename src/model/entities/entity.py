from abc import ABC, abstractmethod


class Entity(ABC):

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    def eat(self) -> None:
        self.hunger = 0

    def __init__(self):
        self.hunger: float = 0
        self.isFed: bool = False

    def getType(self):
        return self.__class__
