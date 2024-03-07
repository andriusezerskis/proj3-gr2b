"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from typing import List
from utils import Point, getPointsInRadius

from model.terrains.tile import Tile
from model.terrains.tiles import Water, Sand

from model.regionHandler import RegionHandler

from parameters import TerrainParameters


class Grid:
    def __init__(self, gridSize: Point) -> None:
        self.tiles: List[List[Tile]] = []
        self.islands: List[List[Tile]] = []
        self.coasts: set[Tile] = set()
        self.gridSize: Point = gridSize
        self.regionHandler = RegionHandler(
            self.gridSize.x(), self.gridSize.y())

    def initialize(self, tiles: List[List[Tile]], islands: List[set[Tile]]) -> None:
        """Random initialization of the grid with perlin noise"""
        self.tiles = tiles
        self.islands = islands

        # construct the set of tiles that will be affected by tides
        for tile in self:
            if Water.getLevel() < tile.height < TerrainParameters.MAX_WATER_LEVEL:
                self.coasts.add(tile)

    def getIsland(self, tile: Tile) -> List[Tile]:
        """Get the island in which the tile is located"""
        for island in self.islands:
            if tile in island:
                return island
        return []

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

            if tile.hasEntity() and not newTile.hasEntity():
                tile.getEntity().kill()
                tile.removeEntity()

            self.coasts.remove(tile)
            self.coasts.add(newTile)

            self.tiles[tile.getPos().y()][tile.getPos().x()] = newTile
            modified.add(newTile)
        return modified

    def updateTemperature(self, tile: Tile) -> None:
        tile.updateTemperature(self.regionHandler.sampleTemperature(
            tile.getPos().x(), tile.getPos().y()))

    def getTile(self, pos: Point) -> Tile:
        if not self.isInGrid(pos):
            raise IndexError(f"Position {pos} is not in the grid")
        return self.tiles[pos.y()][pos.x()]

    def getSize(self):
        return self.gridSize

    def isInGrid(self, pos: Point) -> bool:
        return 0 <= pos.x() < self.gridSize.x() and 0 <= pos.y() < self.gridSize.y()

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
