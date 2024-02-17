import random
from typing import Dict, Type

from constants import EMPTY_TILE_PROBABILITY_GENERATION

from random import random, choices

from model.grid import Grid

from model.entities.algae import Algae
from model.entities.fish import Fish
from model.entities.human import Human
from model.entities.tree import Tree
from model.entities.crab import Crab

from model.terrains.land import Land
from model.terrains.tile import Tile
from model.terrains.water import Water


class EntitiesGenerator:
    ENTITIES_LIST = [Algae, Fish, Human, Tree, Crab]

    def __init__(self):
        self._validEntitiesForTileType = {}

    def generateEntities(self, grid: Grid):
        for tile in grid:
            if random() >= EMPTY_TILE_PROBABILITY_GENERATION:
                self.addRandomEntity(tile)

    def getValidEntities(self, tile: type) -> list[type]:

        if tile not in self._validEntitiesForTileType:
            res = []
            for entityType in self.ENTITIES_LIST:
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



