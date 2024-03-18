"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
import random

from mimesis import Person
from mimesis import Locale
from abc import ABC, abstractmethod

from parameters import EntityParameters, TerrainParameters, DisasterParameters

from model.action import Action
from typing import TypeVar, Type
from utils import Point
from model.drawable import ParametrizedDrawable
from model.crafting.loots import Loot
from overrides import override

from random import choice

from model.movable import Movable

Entity_ = TypeVar("Entity_")
Tile = TypeVar("Tile")
Grid = TypeVar("Grid")


class Entity(Movable, ParametrizedDrawable, ABC):
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
        self._hp = self.getMaxHealthPoints()

        self._name = Person(Locale.FR).first_name()

    @classmethod
    @override
    def _getConfigFilePath(cls) -> str:
        return "../config/entities.json"

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return EntityParameters.TEXTURE_FOLDER_PATH

    @staticmethod
    def getFrenchNameFromClassName(className: str) -> str:
        for cls in Entity.parameterDicts.keys():
            if cls.__name__ == className:
                return cls.getFrenchName()
        raise KeyError

    @classmethod
    def getSpawnWeight(cls) -> float:
        return cls._getParameter("spawn_weight")

    @classmethod
    def getMaxHealthPoints(cls) -> float:
        return cls._getParameter("health_points")

    @classmethod
    def getFrenchName(cls) -> str:
        return cls._getParameter("french_name")

    @classmethod
    def _getValidTiles(cls) -> list[str]:
        return cls._getParameter("valid_tiles")

    @classmethod
    def isValidTileType(cls, tileType: Type[Tile]) -> bool:
        return tileType.__name__ in cls._getValidTiles()

    def getHealthPoints(self) -> float:
        return self._hp

    def canBeEaten(self) -> bool:
        return True

    @classmethod
    def getColor(cls) -> str:
        return cls._getParameter("color")

    @classmethod
    def getSymbol(cls) -> str:
        return cls._getParameter("symbol")

    def getEaten(self) -> bool:
        """
        Make the entity get eaten
        :return: True if the entity dies
        """
        self.kill()
        return True

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
        self._reproductionCooldown = EntityParameters.REPRODUCTION_COOLDOWN
        if other:
            other.reproductionCooldown = EntityParameters.REPRODUCTION_COOLDOWN
        freeTile = choice(self.getValidMovementTiles())
        freeTile.addNewEntity(self.__class__)
        return freeTile

    def isDeadByOldness(self):
        return self._age >= EntityParameters.MAX_AGE

    def isDead(self):
        return self.isDeadByOldness() or self._dead or self._killed

    def kill(self) -> None:
        if self._killed:
            return

        for cls in self.__class__.__mro__:
            self._counts[cls] -= 1

        self._killed = True

    def inflictDamage(self, damage: float) -> None:
        self._hp -= damage
        if self._hp <= 0:
            self.kill()

    def evolve(self) -> bool:
        """
        Makes the entity age
        :return: True if the entity needs to be updated visually
        """
        self._age += 1
        self._reproductionCooldown = max(0, self._reproductionCooldown - 1)

        self._scanSurroundings()
        return False

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
        return self.getAge() // TerrainParameters.DAY_DURATION

    def __str__(self):
        return self.__class__.__name__[0]

    def getAdjacentTiles(self) -> list[Tile]:
        """
        :return: The position of the tiles around the entity
        """
        return self.getGrid().getAdjacentTiles(self.getPos())

    def getValidMovementTiles(self) -> list[Tile]:
        return self._local_information["valid_movement_tiles"]

    @abstractmethod
    def chooseAction(self) -> Action:
        ...

    @override
    def getPos(self) -> Point:
        return self._pos

    def chooseMove(self) -> Point:
        return Point(0, 0)

    def move(self, movement: Point):
        assert not self.getGrid().getTile(self._pos + movement).hasEntity()
        self.getGrid().getTile(self._pos).removeEntity()
        self._pos += movement
        if not self.getGrid().getTile(self._pos).setEntity(self):
            self.kill()

    def setPos(self, pos: Point):
        self._pos = pos
        # self.getGrid().getTile(self._pos).removeEntity()

    @staticmethod
    def getGrid() -> Grid:
        return Entity._grid

    @staticmethod
    def setGrid(grid: Grid):
        Entity._grid = grid

    def setAge(self, age: int):
        self._age = age

    def getTile(self) -> Tile:
        return self.getGrid().getTile(self.getPos())

    def isFitForReproduction(self) -> bool:
        return self.getReproductionCooldown() == 0 and self.getAge() >= EntityParameters.REPRODUCTION_MIN_AGE

    def getReproductionCooldown(self) -> int:
        return self._reproductionCooldown

    @classmethod
    def getCount(cls) -> int:
        if cls not in cls._counts.keys():
            return 0
        return cls._counts[cls]

    @classmethod
    def getLoots(cls):
        return cls._getParameter("loots")

    @classmethod
    def getQuantity(cls, loot):
        assert cls.isValidItemType(loot)
        return cls.getLoots().get(loot.__name__)[0]

    @classmethod
    def getChance(cls, loot):
        assert cls.isValidItemType(loot)
        return cls.getLoots().get(loot.__name__)[1]

    @classmethod
    def isValidItemType(cls, itemType: Type[Loot]) -> bool:
        return itemType.__name__ in cls.getLoots()

    def loot(self):
        res = {}
        for str_loot in self.getLoots():
            tot = 0
            for _ in range(self.getLoots().get(str_loot)[0]):
                tot += 1 if random.random() < self.getLoots().get(str_loot)[
                    1] else 0
            res[str_loot] = tot
        return res
