"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from utils import Point
from typing import TypeVar, Type
from abc import ABC
from overrides import override
from random import choice, choices

from parameters import EntityParameters

from model.entities.entity import Entity
from model.action import Action

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
    def isPrey(cls, prey: Type[Entity]):
        return prey.__name__ in cls._getPreys()

    def getTemperatureDifference(self) -> float:
        return abs(self.getTile().getTemperature() - self.getPreferredTemperature())

    @override
    def evolve(self) -> bool:
        self.hunger += 1 + self.getTemperatureDifference() / 10

        return super().evolve()

    @override
    def _scanSurroundings(self) -> None:
        self._local_information = {"mates": {"adjacent": set(), "viewable": set()},
                                   "preys": {"adjacent": set(), "viewable": set(), "eatable": set()},
                                   "predators": {"adjacent": set(), "viewable": set()},
                                   "valid_movement_tiles": []}

        for tile in self.getGrid().getTilesInRadius(self.getPos(), self.getViewDistance()):
            entity = tile.getEntity()
            if not entity:
                if self.getPos().isNextTo(tile.getPos()) and self.isValidTileType(type(tile)):
                    self._local_information["valid_movement_tiles"].append(
                        tile)
                continue

            if self.isPrey(type(entity)):
                self._local_information["preys"]["viewable"].add(entity)
                if self.getPos().isNextTo(tile.getPos()):
                    self._local_information["preys"]["adjacent"].add(entity)
                    if entity.canBeEaten():
                        self._local_information["preys"]["eatable"].add(entity)

            if isinstance(entity, Animal) and entity.isPrey(type(self)):
                self._local_information["predators"]["viewable"].add(entity)
                if self.getPos().isNextTo(tile.getPos()):
                    self._local_information["predators"]["adjacent"].add(
                        entity)

            if type(entity) is type(self) and entity.isFitForReproduction():
                self._local_information["mates"]["viewable"].add(entity)
                if self.getPos().isNextTo(tile.getPos()):
                    self._local_information["mates"]["adjacent"].add(entity)

    def _scoreMove(self) -> float:
        if not self.canMove():
            return 0

        score = 1

        # incentive to move if predators are nearby
        if len(self._local_information["predators"]["adjacent"]) > 0:
            score += 100
        elif len(self._local_information["predators"]["viewable"]) > 0:
            score += 10

        # incentive to move if the temperature is too bad
        score += self.getTemperatureDifference()

        # incentive to move to find food if hungry
        if len(self._local_information["preys"]["adjacent"]) == 0:
            score += self.getHunger() / 10 + 3 * self.isHungry()

        return score

    def _scoreEat(self) -> float:
        if not self.canEat():
            return 0

        score = 1

        # incentive to eat if hungry
        score += self.isHungry() * 30
        score += self.getHunger() / 5

        return score

    def _scoreReproduce(self) -> float:
        if not self.canReproduce():
            return 0

        # incentive to reproduce if possible
        score = 100

        # disincentive to reproduce if hungry (note that self.canReproduce() is false if the hunger is too high)
        score -= self.hunger / 5

        return max(score, 0)

    @staticmethod
    def _scoreIdle() -> float:
        return 1

    @override
    def chooseAction(self) -> Action:
        move = self._scoreMove()
        eat = self._scoreEat()
        reproduce = self._scoreReproduce()
        idle = self._scoreIdle()
        return choices([Action.MOVE, Action.EAT, Action.REPRODUCE, Action.IDLE],
                       [move, eat, reproduce, idle])[0]

    def choosePrey(self) -> Entity:
        return choice(list(self._local_information["preys"]["eatable"]))

    def canMove(self) -> bool:
        return len(self.getValidMovementTiles()) > 0

    def canEat(self) -> bool:
        return len(self._local_information["preys"]["eatable"]) > 0

    def _scorePosition(self, pos: Point) -> float:
        assert pos.octileDistance(self.getPos()) == 1
        score = 100

        for predator in self._local_information["predators"]["viewable"]:
            if pos.octileDistance(predator.getPos()) == 1:
                # a predator is adjacent
                return 0.1
            elif pos.octileDistance(predator.getPos()) <= self.getViewDistance():
                # a predator is viewable from pos but not adjacent
                score -= 10

        for prey in self._local_information["preys"]["viewable"]:
            if pos.octileDistance(prey.getPos()) == 1:
                # adjacent
                score += 15
            elif pos.octileDistance(prey.getPos()) <= self.getViewDistance():
                # viewable
                score += 10

        for mates in self._local_information["mates"]["viewable"]:
            if pos.octileDistance(mates.getPos()) == 1:
                score += 15
            elif pos.octileDistance(mates.getPos()) <= self.getViewDistance():
                score += 10

        return max(score, 5)

    @override
    def chooseMove(self) -> Point:
        freeTiles = self.getValidMovementTiles()
        assert len(freeTiles) > 0

        scores = []
        for tile in freeTiles:
            scores.append(self._scorePosition(tile.getPos()))

        return choices(freeTiles, scores)[0].getPos() - self.getPos()

    def eat(self, prey: Entity) -> bool:
        self.hunger = 0
        return prey.getEaten()

    @override
    def isDead(self):
        return self.starvedToDeath() or super().isDead()

    @override
    def canReproduce(self) -> bool:
        if not super().canReproduce():
            return False

        if len(self._local_information["mates"]["adjacent"]) == 0:
            # No potential mate
            return False

        return True

    def getMate(self) -> Entity:
        potentialMates = self._local_information["mates"]["adjacent"]
        assert len(potentialMates) > 0
        return choice(list(potentialMates))

    @override
    def reproduce(self, other: Animal_) -> Tile:
        assert other
        return super().reproduce(other)

    @override
    def isFitForReproduction(self) -> bool:
        return super().isFitForReproduction() and self.hunger <= EntityParameters.REPRODUCTION_MAX_HUNGER

    def starvedToDeath(self) -> bool:
        return self.hunger >= EntityParameters.MAX_HUNGER

    def getHunger(self) -> float:
        return self.hunger

    def isHungry(self) -> bool:
        return self.getHunger() > EntityParameters.HUNGRY_THRESHOLD
