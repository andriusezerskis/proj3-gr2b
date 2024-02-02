import random
from typing import List
from model.entitiesGenerator import EntitiesGenerator

from model.gridGenerator import GridGenerator
from model.terrains.tile import Tile
from model.entities.entity import Entity


class Grid:
    def __init__(self, size: tuple) -> None:
        self.tiles: List[Tile] = []
        self.size = size

    def initialize(self):
        """Random initialization of the grid with perlin noise"""
        self.tiles = GridGenerator(self.size[0], self.size[1]).generateGrid()
        entitiesGenerator = EntitiesGenerator()
        entities = entitiesGenerator.generateEntities(self.tiles)
        return entities

    def entitiesInAdjacentTile(self, currentTile) -> List[Entity]:
        """Checks if, given a current tile, there's an entity in an adjacent case to eventually interact with"""
        adjacent_tiles = [
            (currentTile[0] - 1, currentTile[1]),  # up
            (currentTile[0] + 1, currentTile[1]),  # down
            (currentTile[0], currentTile[1] - 1),  # left
            (currentTile[0], currentTile[1] + 1),  # right
            (currentTile[0] - 1, currentTile[1] - 1),  # upper left
            (currentTile[0] - 1, currentTile[1] + 1),  # upper right
            (currentTile[0] + 1, currentTile[1] - 1),  # lower left
            (currentTile[0] + 1, currentTile[1] + 1)  # lower right
        ]
        entitiesList = []
        for tile in adjacent_tiles:
            if 0 <= tile[0] < self.size[0] and 0 <= tile[1] < self.size[1]:
                if self.tiles[tile[0]][tile[1]].getEntity():
                    entitiesList.append(
                        self.tiles[tile[0]][tile[1]].getEntity())

        return entitiesList

    def moveEntity(self, entity, currentTile, nextTile) -> None:
        """Moves an entity from a tile to another"""
        if not self.tiles[nextTile[0]][nextTile[1]].hasEntity():
            self.tiles[nextTile[0]][nextTile[1]].addEntity(entity)
            self.tiles[currentTile[0]][currentTile[1]].removeEntity()

    def randomTileWithoutEntity(self, currentTile):
        """Generate random tile to reproduce, it must be empty and must be the same tile type as the currentTile
        """

        adjacent_tiles = [
            (currentTile.index[0] - 1, currentTile.index[1]),  # up
            (currentTile.index[0] + 1, currentTile.index[1]),  # down
            (currentTile.index[0], currentTile.index[1] - 1),  # left
            (currentTile.index[0], currentTile.index[1] + 1),  # right
            (currentTile.index[0] - 1, currentTile.index[1] - 1),  # upper left
            (currentTile.index[0] - 1,
             currentTile.index[1] + 1),  # upper right
            (currentTile.index[0] + 1, currentTile.index[1] - 1),  # lower left
            (currentTile.index[0] + 1, currentTile.index[1] + 1)  # lower right
        ]

        no_entity = []
        for tile in adjacent_tiles:
            if 0 <= tile[0] < self.size[0] and 0 <= tile[1] < self.size[1]:
                randomTile = self.tiles[tile[0]][tile[1]]
                if not randomTile.getEntity():
                    if (type(currentTile) == type(randomTile)):
                        no_entity.append(
                            self.tiles[tile[0]][tile[1]])
        return no_entity

    def getTiles(self) -> List[List[Tile]]:
        return self.tiles

    def getTile(self, i, j) -> Tile:
        return self.tiles[i][j]

    def __iter__(self):
        for line in self.tiles:
            for tile in line:
                yield tile

    def __str__(self):
        res = ""
        for line in self.tiles:
            for tile in line:
                res += ((str(tile.getEntity()) if tile.getEntity() else '_') + ' ')
            res += "\n"
        return res
