from abc import ABC, abstractmethod

from model.grid import Grid

from utils import Point


class Entity(ABC):
    count = 0
    _grid = None

    def __init__(self, pos: Point):
        self.pos = pos
        Entity.count += 1
        self.age = 0
        self.hunger = 0

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

    @abstractmethod
    def reproduce(self) -> None:
        return True

    def isDeadByOldness(self):
        return self.age >= 10

    def isDead(self):
        return self.isDeadByOldness()

    def evolve(self):
        self.age += 1

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def getHunger(self):
        return self.hunger

    def setHunger(self, hunger: int):
        self.hunger = hunger

    def __str__(self):
        ...

    def getCount(self):
        return self.count

    @staticmethod
    def getGrid() -> Grid:
        return Entity._grid

    @staticmethod
    def setGrid(grid: Grid) -> None:
        Entity.grid = grid
