from abc import ABC, abstractmethod
from constants import ENTITY_MAX_AGE, ENTITY_REPRODUCTION_COOLDOWN, ENTITY_MIN_AGE_REPRODUCTION, DAY_DURATION
from model.action import Action
from typing import TypeVar
from utils import Point

from random import choice

Entity_ = TypeVar("Entity_")
Tile = TypeVar("Tile")
Grid = TypeVar("Grid")


class Entity(ABC):
    count = 0
    _grid = None

    def __init__(self, pos: Point):
        self.pos = pos
        Entity.count += 1
        self.age = 0
        self.reproductionCooldown = 0
        self.reproductionCooldown = 0
        self._validMovementTiles = None
        self._adjacentEntities = None

    def __del__(self):
        Entity.count -= 1

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...



    @staticmethod
    @abstractmethod
    def getValidTiles() -> set[type]:
        ...

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
        self.reproductionCooldown = ENTITY_REPRODUCTION_COOLDOWN
        if other:
            other.reproductionCooldown = ENTITY_REPRODUCTION_COOLDOWN
        freeTile = choice(self.getValidMovementTiles())
        freeTile.addNewEntity(self.__class__)
        return freeTile

    def isDeadByOldness(self):
        return self.age >= ENTITY_MAX_AGE

    def isDead(self):
        return self.isDeadByOldness()

    def evolve(self):
        self.age += 1
        self.reproductionCooldown = max(0, self.reproductionCooldown - 1)
        self._validMovementTiles = None
        self._adjacentEntities = None

    def getAge(self):
        return self.age//DAY_DURATION  # shows age in days instead of steps

    def setAge(self, age):
        self.age = age

    def __str__(self):
        ...

    def getAdjacentTiles(self) -> list[Tile]:
        """
        :return: The position of the tiles around the entity
        """
        return self.getGrid().getAdjacentTiles(self.getPos())

    def getAdjacentEntities(self) -> list[Entity_]:
        if not self._adjacentEntities:
            self._adjacentEntities = [
                tile.getEntity() for tile in self.getAdjacentTiles() if tile.hasEntity()]
        return self._adjacentEntities

    def getFreeAdjacentTiles(self) -> list[Tile]:
        """
        :return: The position of the free tiles around the entity
        """
        return [tile for tile in self.getAdjacentTiles() if not tile.hasEntity()]

    def getValidMovementTiles(self) -> list[Tile]:
        if not self._validMovementTiles:
            self._validMovementTiles = [tile for tile in self.getFreeAdjacentTiles()
                                        if type(tile) in self.getValidTiles()]
        return self._validMovementTiles

    @abstractmethod
    def chooseAction(self) -> Action:
        ...

    def getPos(self) -> Point:
        return self.pos

    def chooseMove(self) -> Point:
        return Point(0, 0)

    def move(self, movement: Point):
        assert not self.getGrid().getTile(self.pos + movement).hasEntity()
        self.getGrid().getTile(self.pos).removeEntity()
        self.pos += movement
        self.getGrid().getTile(self.pos).setEntity(self)

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
        return self.reproductionCooldown

    def getCount(self):
        return self.count
