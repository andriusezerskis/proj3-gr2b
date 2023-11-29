from model.entities.entity import Entity
from abc import abstractmethod, ABC
from overrides import override
from random import random
import random


class Animal(Entity, ABC):

    @staticmethod
    @abstractmethod
    def getClassPreys() -> list:
        return None
    
    @abstractmethod
    def reproduce(self) -> None:
        ...

    def generateLocalPreys(self) -> list:
        preys = []
        for entity_, prob in self.getClassPreys():
            if random.randint(0, 100)/100 <= prob:
                preys.append(entity_)
        return preys

    def __init__(self):
        super().__init__()
        self.preys = self.generateLocalPreys()
