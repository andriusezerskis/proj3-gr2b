import random
from constants import EMPTY_TILE_PROBABILITY_GENERATION

from random import random, choices

from model.grid import Grid

from model.entities.entity import Entity
from model.player.player import Player
from model.terrains.tile import Tile

# these imports are actually necessary, do not trust your IDE
import model.entities.plants
import model.entities.animals


class EntitiesGenerator:

    def __init__(self):
        self.entitySet: set[type] = self._getAllInstanciableEntities()
        print(self.entitySet)
        self._validEntitiesForTileType = {}

    @staticmethod
    def _getAllInstanciableEntities() -> set[type]:
        res = set()
        stack = [Entity]
        while len(stack) > 0:
            current = stack.pop()
            subclasses = current.__subclasses__()
            if len(subclasses) == 0:
                res.add(current)
            else:
                stack.extend(subclasses)
        return res - {Player}

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



