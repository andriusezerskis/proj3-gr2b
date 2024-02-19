"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import random
from constants import EMPTY_TILE_PROBABILITY_GENERATION

from random import random, choices

from model.grid import Grid

from model.generator.automaticGenerator import AutomaticGenerator
from overrides import override

from model.entities.entity import Entity
from model.player.player import Player
from model.terrains.tile import Tile

# these imports are actually necessary, do not trust your IDE
import model.entities.plants
import model.entities.animals


class EntitiesGenerator(AutomaticGenerator):

    def __init__(self):
        self.entitySet: set[type] = self.getTerminalChildrenOfBaseClass()
        self._validEntitiesForTileType = {}

    @classmethod
    @override
    def getBaseClass(cls) -> type:
        return Entity

    @classmethod
    @override
    def getTerminalChildrenOfBaseClass(cls) -> set[type]:
        return super().getTerminalChildrenOfBaseClass() - {Player}

    def generateEntities(self, grid: Grid):
        for tile in grid:
            if random() >= EMPTY_TILE_PROBABILITY_GENERATION:
                self.addRandomEntity(tile)

    def getValidEntities(self, tile: type) -> list[type]:

        if tile not in self._validEntitiesForTileType:
            res = []
            for entityType in self.entitySet:
                assert issubclass(entityType, Entity)
                if entityType.isValidTileType(tile):
                    res.append(entityType)

            self._validEntitiesForTileType[tile] = res

        return self._validEntitiesForTileType[tile]

    def addRandomEntity(self, tile: Tile):
        validEntities = self.getValidEntities(type(tile))
        if len(validEntities) == 0:
            return
        weights = [entityType.getSpawnWeight() for entityType in validEntities]
        return tile.addNewEntity(choices(population=validEntities, weights=weights)[0])
