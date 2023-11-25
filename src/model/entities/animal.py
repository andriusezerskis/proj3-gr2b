from entity import Entity
from abc import abstractmethod, ABC
from random import random


class Animal(Entity, ABC):

    @staticmethod
    @abstractmethod
    def getClassPreys() -> list:
        ...

    def generateLocalPreys(self) -> list:
        preys = []
        for entity_, prob in self.getClassPreys():
            if random() <= prob:
                preys.append(entity_)
        return preys

    def __init__(self):
        super().__init__()
        self.preys = self.generateLocalPreys()
