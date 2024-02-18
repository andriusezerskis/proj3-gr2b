from typing import List
from utils import Point, getPointsInRadius

from model.terrains.tile import Tile
from model.terrains.tiles import Water, Sand

from model.regionHandler import RegionHandler

from constants import MAX_WATER_LEVEL


class Grid:
    def __init__(self, size: Point) -> None:
        self.tiles: List[List[Tile]] = []
        self.islands: List[List[Tile]] = []
        self.coasts: set[Tile] = set()
        self.size: Point = size
        self.regionHandler = RegionHandler(self.size.x(), self.size.y())

    def initialize(self, tiles: List[List[Tile]], islands: List[set[Tile]]) -> None:
        """Random initialization of the grid with perlin noise"""
        self.tiles = tiles
        self.islands = islands

        # construct the set of tiles that will be affected by tides
        for tile in self:
            if Water.getLevel() < tile.height < MAX_WATER_LEVEL:
                self.coasts.add(tile)

    def getTilesInRadius(self, center: Point, radius: int):
        """
        :param center: the center of the circle
        :param radius: the maximum distance from the center
        :return: every point at a distance <= radius from the center WITHOUT including the center
        """
        tiles = []
        for pos in getPointsInRadius(center, radius):
            if self.isInGrid(pos):
                tiles.append(self.getTile(pos))
        return tiles

    def getAdjacentTiles(self, currentTile: Point) -> List[Tile]:
        """
        Equivalent to getTilesInRadius(currentTile, 1)
        :param currentTile: a Point
        :return: every adjacent tiles of currentTile
        """
        return self.getTilesInRadius(currentTile, 1)

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

    def getTemperature(self, pos: Point) -> float:
        return self.regionHandler.sampleTemperature(pos.x(), pos.y())

    def getTile(self, pos: Point) -> Tile:
        if not self.isInGrid(pos):
            raise IndexError
        return self.tiles[pos.y()][pos.x()]

    def getSize(self):
        return self.size

    def isInGrid(self, pos: Point) -> bool:
        return 0 <= pos.x() < self.size.x() and 0 <= pos.y() < self.size.y()

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
