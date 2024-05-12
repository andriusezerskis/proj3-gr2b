from abc import ABC
from typing import Type
import random

from model.grid import Grid
from model.terrains.tile import Tile
from model.generator.gridGenerator import GridGenerator
from model.entities.entity import Entity
from utils import Point, getTerminalSubclassesOfClass
from parameters import EntityParameters


class GridLoader(ABC):
    symbolsToType = dict()

    @classmethod
    def _generateSymbolsToType(cls):
        for instanciable in getTerminalSubclassesOfClass(Entity):
            cls.symbolsToType[instanciable.getSymbol()] = instanciable

    @classmethod
    def _getEntityTypeFromSymbol(cls, symbol: str) -> Type[Entity] | None:
        if len(cls.symbolsToType) == 0:
            cls._generateSymbolsToType()

        if symbol not in cls.symbolsToType:
            return None

        return cls.symbolsToType[symbol]

    @classmethod
    def loadFromFile(cls, path: str) -> Grid:

        with open(path, "r") as f:
            height = int(f.readline())
            width = int(f.readline())

            gridSize = Point(width, height)

            f.readline()

            mat: list[list[Tile]] = []

            for y in range(height):
                mat.append([])
                for x, level in enumerate(f.readline().strip().split(" ")):
                    mat[y].append(GridGenerator.getTileFromHeight(x, y, float(level)))

            f.readline()

            for y in range(height):
                for x, symbol in enumerate(f.readline().strip().split(" ")):
                    entityType = cls._getEntityTypeFromSymbol(symbol)
                    if entityType:
                        mat[y][x].addNewEntity(entityType, random.randint(0, EntityParameters.MAX_AGE))

        grid = Grid(gridSize)
        grid.initialize(mat, GridGenerator.getIslands(mat, gridSize, (-1,)))
        return grid
