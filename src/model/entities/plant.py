from model.entities.entity import Entity
from abc import ABC
from abc import abstractmethod
from random import random


class Plant(Entity, ABC):
    @abstractmethod
    def reproduce(self) -> None:
        ...
