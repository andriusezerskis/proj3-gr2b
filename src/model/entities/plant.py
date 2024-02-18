from model.entities.entity import Entity
from abc import ABC
from overrides import override
from random import random
from model.action import Action
from constants import PLANT_REPRODUCTION_PROBABILITY


class Plant(Entity, ABC):

    @override
    def chooseAction(self) -> Action:
        if random() < PLANT_REPRODUCTION_PROBABILITY and len(self.getValidMovementTiles()) > 0:
            return Action.REPRODUCE
        return Action.IDLE
