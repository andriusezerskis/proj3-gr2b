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
        self.reproductionCooldown = 0

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
        # self.age += 1
        self.reproductionCooldown = max(0, self.reproductionCooldown - 1)

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

    def getAdjacentTiles(self) -> list["Tile"]:
        """
        :return: The position of the tiles around the entity
        """
        return self.getGrid().getAdjacentTiles(self.getPos())

    def getFreeAdjacentTiles(self) -> list["Tile"]:
        """
        :return: The position of the free tiles around the entity
        """
        return [tile for tile in self.getAdjacentTiles() if not tile.hasEntity()]

    def getValidMovementTiles(self) -> list["Tile"]:
        return [tile for tile in self.getFreeAdjacentTiles() if type(tile) in self.getValidTiles()]

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
    def getGrid() -> "Grid":
        return Entity._grid

    @staticmethod
    def setGrid(grid: "Grid"):
        Entity._grid = grid

    def getCount(self):
        return self.count
