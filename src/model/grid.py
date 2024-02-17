from typing import List
from utils import Point, getPointsAdjacentTo

from model.terrains.tile import Tile
from model.terrains.sand import Sand
from model.terrains.water import Water

from constants import WATER_LEVEL, MAX_WATER_LEVEL


class Grid:
    def __init__(self, size: Point) -> None:
        self.tiles: List[List[Tile]] = []
        self.islands: List[List[Tile]] = []
        self.coasts: set[Tile] = set()
        self.size: Point = size

    def initialize(self, tiles: List[List[Tile]], islands: List[set[Tile]]) -> None:
        """Random initialization of the grid with perlin noise"""
        self.tiles = tiles
        self.islands = islands

        # construct the set of tiles that will be affected by tides
        for tile in self:
            if WATER_LEVEL < tile.height < MAX_WATER_LEVEL:
                self.coasts.add(tile)

    def getAdjacentTiles(self, currentTile: Point) -> List[Tile]:
        tiles = []
        for pos in getPointsAdjacentTo(currentTile):
            if self.isPosInGrid(pos):
                tiles.append(self.getTile(pos))
        return tiles

    def updateTilesWithWaterLevel(self, newWaterLevel: float) -> set[Tile]:
        modified = set()
        for tile in self.coasts:
            newTile = None
            if type(tile) is Sand and tile.height < newWaterLevel:
                newTile = Tile.copyWithDifferentTypeOf(tile, Water)
            elif type(tile) is Water and tile.height > newWaterLevel:
                newTile = Tile.copyWithDifferentTypeOf(tile, Sand)

            if not newTile:
                continue

            self.coasts.remove(tile)
            self.coasts.add(newTile)

            self.tiles[tile.getPos().y()][tile.getPos().x()] = newTile
            modified.add(newTile)
        return modified

    def getTile(self, pos: Point) -> Tile:
        if not self.isPosInGrid(pos):
            raise IndexError
        return self.tiles[pos.y()][pos.x()]

    def getSize(self):
        return self.size

    def isPosInGrid(self, pos: Point) -> bool:
        return 0 <= pos.x() < self.size.x() and 0 <= pos.y() < self.size.y()

    #@staticmethod
    def isInGrid(self, i, j):
        return 0 <= i < self.size.x() and 0 <= j < self.size.y()

    def __iter__(self):
        for line in self.tiles:
            for tile in line:
                yield tile

    def __str__(self):
        res = ""
        for line in self.tiles:
            for tile in line:
                # res += ((str(tile.getEntity()) if tile.getEntity() else '_') + ' ')
                res += (str(tile) + ' ')
            res += "\n"
        return res
