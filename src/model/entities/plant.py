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
from parameters.constants import (PLANT_REPRODUCTION_PROBABILITY, PLANT_ADJACENT_PEERS_AUTO_DEATH_THRESHOLD,
                                  PLANT_PROBABILITY_DEATH_IF_TOO_MUCH_PEERS)


class Plant(Entity, ABC):

    @override
    def chooseAction(self) -> Action:
        adjacentPeers = len([tile for tile in self.getAdjacentTiles()
                             if tile.hasEntity() and type(self) is type(tile.getEntity())])

        if (adjacentPeers >= PLANT_ADJACENT_PEERS_AUTO_DEATH_THRESHOLD and
                random() < PLANT_PROBABILITY_DEATH_IF_TOO_MUCH_PEERS):
            return Action.DIE

        probability = PLANT_REPRODUCTION_PROBABILITY - 0.01 * adjacentPeers

        if random() < probability and len(self.getValidMovementTiles()) > 0:
            return Action.REPRODUCE

        return Action.IDLE
