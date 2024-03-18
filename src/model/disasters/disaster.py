from abc import ABC, abstractmethod

from typing import TypeVar

Tile = TypeVar("Tile")


class Disaster(ABC):

    @classmethod
    @abstractmethod
    def getTexturePath(cls):
        ...

    @classmethod
    @abstractmethod
    def getMaxDamage(cls):
        ...

    @classmethod
    @abstractmethod
    def getMaxTemperatureDifference(cls):
        ...

    @classmethod
    @abstractmethod
    def getDuration(cls):
        ...

    def getStrength(self):
        return self._strength

    def decreaseStrength(self):
        self._strength = max(0., self._strength - 1 / self.getDuration())

    def getDamagePoints(self):
        return self.getStrength() * self.getMaxDamage()

    def getTemperature(self):
        return self.getStrength() * self.getMaxTemperatureDifference()

    @classmethod
    def applyDisaster(cls, tile: Tile, strength: float = 1) -> None:
        tile.setDisaster(cls(strength))

    def __init__(self, strength: float):
        super().__init__()
        self._strength = strength
