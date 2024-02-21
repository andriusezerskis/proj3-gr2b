"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC
from overrides import override
from random import random

from model.entities.entity import Entity
from model.action import Action
from constants import PLANT_REPRODUCTION_PROBABILITY


class Plant(Entity, ABC):

    @override
    def chooseAction(self) -> Action:
        if random() < PLANT_REPRODUCTION_PROBABILITY and len(self.getValidMovementTiles()) > 0:
            return Action.REPRODUCE
        return Action.IDLE
