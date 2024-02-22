"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from mimesis import Person
from mimesis import Locale
from abc import ABC, abstractmethod
from constants import (ENTITY_MAX_AGE, ENTITY_REPRODUCTION_COOLDOWN, ENTITY_MIN_AGE_REPRODUCTION, DAY_DURATION,
                       ENTITY_PARAMETERS, ENTITIES_TEXTURE_FOLDER_PATH)
from model.action import Action
from typing import TypeVar
from utils import Point
from model.drawable import ParametrizedDrawable
from overrides import override

from random import choice

Entity_ = TypeVar("Entity_")
Tile = TypeVar("Tile")
Grid = TypeVar("Grid")


class Entity(ParametrizedDrawable, ABC):
    # https://stackoverflow.com/a/75663885
    _counts = dict()
    _grid = None

    def __init__(self, pos: Point):
        super().__init__()

        for cls in self.__class__.__mro__:
            if cls not in self._counts.keys():
                self._counts[cls] = 0
            self._counts[cls] += 1

        self._pos = pos
        self._age = 0
        self._reproductionCooldown = 0
        self._local_information = {}
        self._dead = False
        self._killed = False

        self._name = Person(Locale.FR).first_name()

    @classmethod
    @override
    def _getParameters(cls) -> dict:
        return ENTITY_PARAMETERS

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return ENTITIES_TEXTURE_FOLDER_PATH

    @classmethod
    def getSpawnWeight(cls) -> float:
        return cls._getParameter("spawn_weight")
    
    @classmethod
    def getHealthPoints(cls) -> float:
        return cls._getParameter("health_points")

    @classmethod
    def _getValidTiles(cls) -> list[str]:
        return cls._getParameter("valid_tiles")

    @classmethod
    def isValidTileType(cls, tileType: type) -> bool:
        return tileType.__name__ in cls._getValidTiles()

    def canReproduce(self) -> bool:
        """
        :return: whether the entity can reproduce and with which entity it can do so
        """
        return self.isFitForReproduction() and len(self.getValidMovementTiles()) > 0

    def reproduce(self, other: Entity_ | None) -> Tile:
        """
        Reproduces and places the newborn in the grid
        :return: the position of the newborn
        """
        self._reproductionCooldown = ENTITY_REPRODUCTION_COOLDOWN
        if other:
            other.reproductionCooldown = ENTITY_REPRODUCTION_COOLDOWN
        freeTile = choice(self.getValidMovementTiles())
        freeTile.addNewEntity(self.__class__)
        return freeTile

    def isDeadByOldness(self):
        return self._age >= ENTITY_MAX_AGE

    def isDead(self):
        return self.isDeadByOldness() or self._dead

    def kill(self) -> None:
        if self._killed:
            return

        for cls in self.__class__.__mro__:
            self._counts[cls] -= 1

        self._killed = True

    def evolve(self):
        self._age += 1
        self._reproductionCooldown = max(0, self._reproductionCooldown - 1)

        self._scanSurroundings()

    def _scanSurroundings(self) -> None:
        self._local_information = {"valid_movement_tiles": []}

        for tile in self.getAdjacentTiles():
            if not tile.hasEntity() and self.getPos().isNextTo(tile.getPos()) and self.isValidTileType(type(tile)):
                self._local_information["valid_movement_tiles"].append(tile)

    def getAge(self) -> int:
        return self._age

    def getName(self) -> str:
        return self._name

    def getDisplayAge(self) -> int:
        return self.getAge() // DAY_DURATION

    def __str__(self):
        return self.__class__.__name__[0]

    def getAdjacentTiles(self) -> list[Tile]:
        """
        :return: The position of the tiles around the entity
        """
        return self.getGrid().getAdjacentTiles(self.getPos())

    def getValidMovementTiles(self) -> list[Tile]:
        return self._local_information["valid_movement_tiles"]

    def setDead(self, dead):
        self._dead = dead

    @abstractmethod
    def chooseAction(self) -> Action:
        ...

    def getPos(self) -> Point:
        return self._pos

    def chooseMove(self) -> Point:
        return Point(0, 0)

    def move(self, movement: Point):
        assert not self.getGrid().getTile(self._pos + movement).hasEntity()
        self.getGrid().getTile(self._pos).removeEntity()
        self._pos += movement
        self.getGrid().getTile(self._pos).setEntity(self)

    @staticmethod
    def getGrid() -> Grid:
        return Entity._grid

    @staticmethod
    def setGrid(grid: Grid):
        Entity._grid = grid

    def getTile(self) -> Tile:
        return self.getGrid().getTile(self.getPos())

    def isFitForReproduction(self) -> bool:
        return self.getReproductionCooldown() == 0 and self.getAge() >= ENTITY_MIN_AGE_REPRODUCTION

    def getReproductionCooldown(self) -> int:
        return self._reproductionCooldown

    @classmethod
    def getCount(cls) -> int:
        return cls._counts[cls]
