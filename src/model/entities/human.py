from model.entities.animal import Animal
from overrides import override

from utils import Point

from model.entities.fish import Fish
from model.entities.tree import Tree

from model.terrains.land import Land
from model.terrains.sand import Sand

from constants import HUMAN_TEXTURE_PATH, PREFERRED_TEMPERATURE_HUMAN


class Human(Animal):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Human.count += 1

    def __del__(self):
        super().__del__()
        Human.count -= 1
        
    @staticmethod
    @override
    def getTexturePath() -> str:
        return HUMAN_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Land, Sand}

    @staticmethod
    def getPreferredTemperature() -> float:
        return PREFERRED_TEMPERATURE_HUMAN

    @staticmethod
    @override
    def getPreys() -> set[type]:
        return {Fish, Tree}
  
    def __str__(self):
        return 'H'
  