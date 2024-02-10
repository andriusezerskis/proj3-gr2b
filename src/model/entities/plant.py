from model.entities.entity import Entity
from abc import ABC
from abc import abstractmethod
from random import random


class Plant(Entity, ABC):
    count = 0

    def __init__(self):
        super().__init__()
        Plant.count += 1

    def __del__(self):
        super().__del__()
        Plant.count -= 1

    def reproduce(self) -> None:
        return True if random() < 0.5 else False
