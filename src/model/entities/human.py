import random
from model.action import Action
from model.entities.animal import Animal
from overrides import override

from utils import Point

from model.entities.fish import Fish
from model.entities.tree import Tree

from model.terrains.land import Land
from model.terrains.sand import Sand

from constants import HUMAN_TEXTURE_PATH


class Human(Animal):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Human.count += 1
        self.woodNumber = 0

    def __del__(self):
        super().__del__()
        Human.count -= 1

    @override
    def chooseAction(self) -> Action:
        if self.hasEnoughWood():
            return Action.BUILD_BOAT

        if self.canCutWood():
            return Action.CUT_WOOD

        if self.isHungry() and self.canEat():
            return Action.EAT

        if self.canReproduce():
            return Action.REPRODUCE

        freeTiles = self.getValidMovementTiles()
        if len(freeTiles) == 0:
            return Action.IDLE

        return Action.MOVE

    def canCutWood(self) -> bool:
        return len(self.getAdjacentWood()) > 0

    def cutWood(self, tree):
        self.woodNumber += 1
        print("cut wood")
        tree.getTile().removeEntity()

    def getAdjacentWood(self):
        return [x for x in self.getAdjacentPreys() if isinstance(x, Tree)]

    def hasEnoughWood(self) -> bool:
        return self.woodNumber >= 1

    def buildBoat(self):
        self.woodNumber -= 1

        print("build boat")
        return random.choice(self.getFreeAdjacentTiles())

    @staticmethod
    @override
    def getTexturePath() -> str:
        return HUMAN_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Land, Sand}

    @staticmethod
    @override
    def getPreys() -> set[type]:
        return {Fish, Tree}

    def __str__(self):
        return 'H'
