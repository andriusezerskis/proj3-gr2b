from model.entities.entity import Entity
from abc import ABC
from abc import abstractmethod
from utils import Point
from overrides import override
from random import random
from model.action import Action


class Plant(Entity, ABC):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Plant.count += 1

    def __del__(self):
        super().__del__()
        Plant.count -= 1

    @override
    def chooseAction(self) -> Action:
        if random() < 0.1 and len(self.getValidMovementTiles()) > 0:
            return Action.REPRODUCE
        return Action.IDLE
