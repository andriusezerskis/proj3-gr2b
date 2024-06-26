"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from typing import Type

from model.generator.noiseGenerator import NoiseGenerator
from model.terrains.tile import Tile
from model.grid import Grid

from model.generator.automaticGenerator import AutomaticGenerator
from overrides import override

# again, this import seems useless but is not
import model.terrains.tiles
from model.terrains.tiles import Water

from utils import Point


class GridGenerator(AutomaticGenerator):

    _thresholds: list[tuple[Type[Tile], float]] = []
    _ranges: dict[Type[Tile]: tuple[float, float]] = {}

    def __init__(self, gridSize: Point, islandNb: list[int], islandSize: int):
        """
        :param gridSize: x: width of the map, y: height of the map
        :param islandNb: number of islands in the grid (an array of possible values)
        :param islandSize: minimal number of land tiles in an island
        """
        self.noiseGenerator = None
        self.gridSize = gridSize
        self.matrix = None
        self.islandNb = islandNb
        self.islandSize = islandSize
        self.generateThresholds()
        self.maxAbsHeight = 0

    @classmethod
    @override
    def getBaseClass(cls) -> Type[Tile]:
        return Tile

    @classmethod
    def generateThresholds(cls) -> None:
        tileTypes = cls.getTerminalChildrenOfBaseClass()
        res = []
        for tileType in tileTypes:
            res.append((tileType, tileType.getLevel()))

        cls._thresholds = sorted(res, key=lambda x: x[1])

    # maybe move this inside an attribute/property of the future Constant class?
    @classmethod
    def getRange(cls, tileType: Type[Tile]) -> tuple[float, float]:
        if tileType in cls._ranges:
            return cls._ranges[tileType]

        if len(cls._thresholds) == 0:
            cls.generateThresholds()

        res: tuple[float, float] = (-1, -1)
        for tile, level in cls._thresholds:
            oldMax = res[1]
            res = oldMax, level
            if tile is tileType:
                break

        cls._ranges[tileType] = res
        return tuple(res)

    @classmethod
    def getTileFromHeight(cls, x: int, y: int, height: float) -> Tile:
        if len(cls._thresholds) == 0:
            cls.generateThresholds()

        for tileType, threshold in cls._thresholds:
            if height <= threshold:
                return tileType(Point(x, y), height)

    def _getTile(self, x: int, y: int) -> Tile:
        sample = self.noiseGenerator.sample2D(
            x/self.gridSize.x(), y/self.gridSize.y()) / self.maxAbsHeight

        return self.getTileFromHeight(x, y, sample)

    def _generateMatrix(self) -> list[list[Tile]]:
        return [[self._getTile(x, y) for x in range(self.gridSize.x())] for y in range(self.gridSize.y())]

    @classmethod
    def getIslands(cls, matrix, gridSize, islandNb=(-1,)) -> list[set[Tile]]:
        islands = []
        visited = set()
        for y, row in enumerate(matrix):
            for x, tile in enumerate(row):
                if type(tile) is not Water and tile not in visited:

                    # new island found
                    if islandNb != (-1,) and len(islands) >= max(islandNb):
                        # no need to look further, we've found too many islands
                        return []

                    visited.add(tile)
                    island = set()

                    cls._getIsland(matrix, gridSize, x, y, island, visited)
                    islands.append(island)

                else:
                    visited.add(tile)

        return islands

    @classmethod
    def _getIsland(cls, matrix, gridSize, x: int, y: int, island: set[Tile], visited: set[Tile]) -> None:
        stack = [(x, y)]
        while len(stack) > 0:
            x, y = stack.pop()
            island.add(matrix[y][x])
            for newx, newy in [(x + offsetx, y + offsety) for offsetx in [-1, 0, 1] for offsety in [-1, 0, 1]]:
                if (0 <= newx < gridSize.x() and 0 <= newy < gridSize.y() and matrix[newy][newx] not in visited and
                        type(matrix[newy][newx]) is not Water):
                    visited.add(matrix[newy][newx])
                    stack.append((newx, newy))

    def getNormalizationBorns(self) -> None:
        self.maxAbsHeight = 0
        for y in range(self.gridSize.y()):
            for x in range(self.gridSize.x()):
                sample = self.noiseGenerator.sample2D(
                    x/self.gridSize.x(), y/self.gridSize.y())
                self.maxAbsHeight = max(self.maxAbsHeight, abs(sample))

    def generateGrid(self) -> Grid:
        islands = []
        sizeOk = False
        start = time.time()
        print("Generating terrain...")
        while len(islands) not in self.islandNb or not sizeOk:
            self.noiseGenerator = NoiseGenerator()
            self.noiseGenerator.addNoise(2, 1)
            self.noiseGenerator.addNoise(4, 0.5)
            self.getNormalizationBorns()
            self.matrix = self._generateMatrix()
            islands = self.getIslands(
                self.matrix, self.gridSize, self.islandNb)
            sizeOk = True
            for island in islands:
                if len(island) < self.islandSize:
                    sizeOk = False
                    break

        grid = Grid(self.gridSize)
        grid.initialize(self.matrix, islands)
        print("Terrain generated in ", time.time() - start, "s")
        return grid
