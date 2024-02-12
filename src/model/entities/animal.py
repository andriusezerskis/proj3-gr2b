from typing import List

from utils import Point

from model.entities.entity import Entity
from abc import abstractmethod, ABC
from overrides import override
from random import choice
import random


class Animal(Entity, ABC):
    count = 0

    def __init__(self):
        super().__init__()
        Animal.count += 1
        self.hunger: float = 5
        self.age = 0

    def __del__(self):
        super().__del__()
        Animal.count -= 1

    @override
    def chooseMove(self) -> Point:
        return choice(self.getAdjacentTiles()) - self.getPos()

    @staticmethod
    @abstractmethod
    def getPreys() -> set[type]:
        ...

    @override
    def isDead(self):
        return self.starvedToDeath() or self.isDeadByOldness()

    @override
    def evolve(self):
        super().evolve()
        self.hunger += 1

    def reproduce(self):
        return True if self.hunger < 5 < self.age else False

    def starvedToDeath(self) -> bool:
        return self.hunger > 9

    def eat(self) -> None:
        if self.hunger > 0:
            # diminish hunger depending on the entity eaten (?)
            self.hunger = 0
