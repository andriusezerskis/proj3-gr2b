from typing import List

from model.entities.entity import Entity
from abc import abstractmethod, ABC
from overrides import override
from random import random
import random


class Animal(Entity, ABC):
    def __init__(self):
        super().__init__()
        self.preys = self.generateLocalPreys()
        self.hunger: float = 5
        self.age = 0

    @staticmethod
    @abstractmethod
    def getClassPreys() -> list:
        return []

    @override
    def isDead(self):
        return self.starvedToDeath() or self.isDeadByOldness()

    @override
    def evolve(self):
        self.age += 1
        self.hunger += 1

    def reproduce(self):
        return True if self.hunger < 5 and self.age > 5 else False

    def generateLocalPreys(self) -> List[Entity]:
        preys = []
        for entity_, prob in self.getClassPreys():
            if random.randint(0, 100)/100 <= prob:
                preys.append(entity_)
        return preys

    def starvedToDeath(self) -> bool:
        return self.hunger > 9

    def eat(self) -> None:
        if self.hunger > 0:
            # diminish hunger depending on the entity eaten (?)
            self.hunger = 0
