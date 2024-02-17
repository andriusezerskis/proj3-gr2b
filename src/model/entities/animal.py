from utils import Point
from typing import TypeVar
from model.entities.entity import Entity
from model.action import Action
from abc import ABC
from overrides import override
from random import choice, choices
from constants import ENTITY_MAX_HUNGER, ENTITY_MAX_HUNGER_REPRODUCTION, ENTITY_HUNGRY_THRESHOLD

Tile = TypeVar("Tile")
Animal_ = TypeVar("Animal_")


class Animal(Entity, ABC):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.hunger: float = 0

        self._local_information = {}

    @classmethod
    def _getPreys(cls) -> list[str]:
        return cls._getParameter("preys")

    @classmethod
    def getPreysNames(cls) -> list[str]:
        return cls._getPreys()

    @classmethod
    def getViewDistance(cls) -> int:
        return cls._getParameter("view_distance")

    @classmethod
    def getPreferredTemperature(cls) -> float:
        return cls._getParameter("preferred_temperature")

    @classmethod
    def isPrey(cls, prey: type):
        return prey.__name__ in cls._getPreys()

    def getTemperatureDifference(self) -> float:
        return abs(self.getGrid().getTemperature(self.getPos()) - self.getPreferredTemperature())

    @override
    def evolve(self):
        super().evolve()
        self._local_information = {"mates": {"adjacent": set(), "viewable": set()},
                                   "preys": {"adjacent": set(), "viewable": set()},
                                   "predators": {"adjacent": set(), "viewable": set()}}
        self.hunger += 1 + self.getTemperatureDifference() / 10

    def _scanSurroundings(self) -> None:
        for tile in self.getGrid().getTilesInRadius(self.getPos(), self.getViewDistance()):
            entity = tile.getEntity()
            if not entity:
                continue

            if self.isPrey(type(entity)):
                self._local_information["preys"]["viewable"].add(entity)
                if self.getPos().octileDistance(tile.getPos()) == 1:
                    self._local_information["preys"]["adjacent"].add(entity)

            if isinstance(entity, Animal) and entity.isPrey(type(self)):
                self._local_information["predators"]["viewable"].add(entity)
                if self.getPos().octileDistance(tile.getPos()) == 1:
                    self._local_information["predators"]["adjacent"].add(entity)

            if type(entity) is type(self) and entity.isFitForReproduction():
                self._local_information["mates"]["viewable"].add(entity)
                if self.getPos().octileDistance(tile.getPos()) == 1:
                    self._local_information["mates"]["adjacent"].add(entity)

    def _scoreMove(self) -> float:
        return 1

    def _scoreEat(self) -> float:
        return 1

    def _scoreReproduce(self) -> float:
        return 1

    @staticmethod
    def _scoreIdle() -> float:
        return 1

    @override
    def chooseAction(self) -> Action:
        self._scanSurroundings()

        move = self._scoreMove()
        eat = self._scoreEat()
        reproduce = self._scoreReproduce()
        idle = self._scoreIdle()

        if self.isHungry() and self.canEat():
            return Action.EAT

        if self.canReproduce():
            return Action.REPRODUCE

        freeTiles = self.getValidMovementTiles()
        if len(freeTiles) == 0:
            return Action.IDLE

        return Action.MOVE

        return choices([Action.MOVE, Action.EAT, Action.REPRODUCE, Action.IDLE],
                       [move, eat, reproduce, idle])[0]

    def choosePrey(self) -> Entity:
        return choice(list(self._local_information["preys"]["adjacent"]))

    def canEat(self) -> bool:
        return len(self._local_information["preys"]["adjacent"]) > 0

    @override
    def chooseMove(self) -> Point:
        freeTiles = self.getValidMovementTiles()
        assert len(freeTiles) > 0
        return choice(freeTiles).getPos() - self.getPos()

    def eat(self, prey: Entity):
        self.hunger = 0
        prey.setDead(True)
        prey.getTile().removeEntity()

    @override
    def isDead(self):
        return self.starvedToDeath() or self.isDeadByOldness() or self.dead

    @override
    def canReproduce(self) -> bool:
        if not super().canReproduce():
            return False

        potentialMates = self._local_information["mates"]["adjacent"]
        if len(potentialMates) == 0:
            # No potential mate
            return False

        return True

    def getMate(self) -> Entity:
        potentialMates = self._local_information["mates"]["adjacent"]
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

    def getHunger(self) -> float:
        return self.hunger

    def isHungry(self) -> bool:
        return self.getHunger() > ENTITY_HUNGRY_THRESHOLD
