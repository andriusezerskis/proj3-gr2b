from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self):

        self.age = 0
        self.hunger = 0

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    @staticmethod
    @abstractmethod
    def getValidTiles() -> set[type]:
        ...

    @abstractmethod
    def reproduce(self) -> None:
        return True

    def isDeadByOldness(self):
        return self.age >= 10

    def isDead(self):
        return self.isDeadByOldness()

    def evolve(self):
        self.age += 1

    def __str__(self):
        ...
