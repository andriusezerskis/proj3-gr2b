from abc import ABC, abstractmethod

from model.action import Action

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
        ...

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

    def getAdjacentTiles(self) -> list[Point]:
        """
        :return: The position of the tiles around the entity
        """
        return self.getGrid().getAdjacentTiles(self.getPos())

    def getFreeAdjacentTiles(self) -> list[Point]:
        """
        :return: The position of the free tiles around the entity
        """
        return [tile for tile in self.getAdjacentTiles() if not self.getGrid().getTile(tile).hasEntity()]

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

    def getCount(self):
        return self.count

    @staticmethod
    def getGrid() -> "Grid":
        return Entity._grid

    @staticmethod
    def setGrid(grid: "Grid") -> None:
        Entity._grid = grid
