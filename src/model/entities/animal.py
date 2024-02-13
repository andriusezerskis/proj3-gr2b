from utils import Point
from typing import TypeVar
from model.entities.entity import Entity
from model.action import Action
from abc import abstractmethod, ABC
from overrides import override
from random import choice
from constants import ENTITY_MAX_HUNGER, ENTITY_MAX_HUNGER_REPRODUCTION

Tile = TypeVar("Tile")
Animal_ = TypeVar("Animal_")


class Animal(Entity, ABC):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Animal.count += 1
        self.hunger = 0

        self._potentialMates = None

    def __del__(self):
        super().__del__()
        Animal.count -= 1

    @override
    def chooseAction(self) -> Action:
        if self.canReproduce():
            return Action.REPRODUCE

        freeTiles = self.getValidMovementTiles()
        if len(freeTiles) == 0:
            return Action.IDLE

        return Action.MOVE

    @override
    def chooseMove(self) -> Point:
        freeTiles = self.getValidMovementTiles()
        assert len(freeTiles) > 0
        return choice(freeTiles).getPos() - self.getPos()

    @staticmethod
    @abstractmethod
    def getPreys() -> set[type]:
        ...

    @override
    def isDead(self):
        return self.starvedToDeath() or self.isDeadByOldness()

    @override
    def evolve(self):
        super().evolve()
        self._potentialMates = None
        # self.hunger += 1

    def getPotentialMates(self) -> list[Entity]:
        if not self._potentialMates:
            self._potentialMates = [tile for tile in self.getAdjacentTiles()
                                    if type(tile.getEntity()) == type(self) and tile.getEntity().isFitForReproduction()]
        return self._potentialMates

    @override
    def canReproduce(self) -> bool:
        if not self.isFitForReproduction():
            return False

        potentialMates = self.getPotentialMates()
        if len(potentialMates) == 0:
            # No potential mate
            return False

        babyTiles = self.getValidMovementTiles()
        if len(babyTiles) == 0:
            # No tile to place the newborn
            return False

        return True

    def getMate(self) -> Entity:
        potentialMates = self.getPotentialMates()
        assert len(potentialMates) > 0
        return choice(potentialMates)

    @override
    def reproduce(self, other: Animal_) -> Tile:
        assert other
        return super().reproduce(other)

    @override
    def isFitForReproduction(self) -> bool:
        return super().isFitForReproduction() and self.hunger <= ENTITY_MAX_HUNGER_REPRODUCTION

    def starvedToDeath(self) -> bool:
        return self.hunger >= ENTITY_MAX_HUNGER

    def getHunger(self) -> int:
        return self.hunger

    def eat(self) -> None:
        if self.hunger > 0:
            # diminish hunger depending on the entity eaten (?)
            self.hunger = 0
