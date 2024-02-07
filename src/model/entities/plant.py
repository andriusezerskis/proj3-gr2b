from model.entities.entity import Entity
from abc import ABC
from abc import abstractmethod
from random import random


class Plant(Entity, ABC):

    def reproduce(self) -> None:
        return True if random() < 0.5 else False
