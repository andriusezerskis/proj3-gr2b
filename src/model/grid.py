import random
from typing import List

from utils import Point, getPointsAdjacentTo

from model.entitiesGenerator import EntitiesGenerator

from model.gridGenerator import GridGenerator
from model.terrains.tile import Tile
from model.entities.entity import Entity


class Grid:
    def __init__(self, size: Point) -> None:
        self.tiles: List[List[Tile]] = []
        self.islands: List[Tile] = []
        self.size: Point = size

    def initialize(self):
        """Random initialization of the grid with perlin noise"""
        self.tiles, self.islands = GridGenerator(self.size.x(), self.size.y(),
                                                 [2, 3, 4, 5, 6], 350).generateGrid()
        entitiesGenerator = EntitiesGenerator()
        entities = entitiesGenerator.generateEntities(self.tiles)
        return entities

    def entitiesInAdjacentTile(self, currentTile: Point) -> List[Entity]:
        """Checks if, given a current tile, there's an entity in an adjacent case to eventually interact with"""
        entitiesList = []
        for pos in getPointsAdjacentTo(currentTile):
            if self.isPosInGrid(pos) and self.getTile(pos).getEntity():
                entitiesList.append(self.getTile(pos).getEntity())

        return entitiesList

    def moveEntity(self, entity, currentTile: Point, nextTile: Point) -> None:
        """Moves an entity from a tile to another"""
        if not self.getTile(currentTile).hasEntity():
            self.getTile(nextTile).addEntity(entity)
            self.getTile(currentTile).removeEntity()

    def randomTileWithoutEntity(self, currentTile: Point):
        """Generate random tile to reproduce, it must be empty and must be the same tile type as the currentTile
        """

        no_entity = []
        for tile in getPointsAdjacentTo(currentTile):
            if self.isPosInGrid(tile):
                randomTile = self.getTile(tile)
                if not randomTile.getEntity():
                    if type(currentTile) is type(randomTile):
                        no_entity.append(
                            self.getTile(tile))
        return no_entity

    def getTiles(self) -> List[List[Tile]]:
        return self.tiles

    def getTile(self, pos: Point) -> Tile:
        return self.tiles[pos.y()][pos.x()]

    def isPosInGrid(self, pos: Point) -> bool:
        return 0 <= pos.x() < self.size.x() and 0 <= pos.y() < self.size.y()

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
