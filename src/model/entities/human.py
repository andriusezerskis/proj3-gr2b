from model.entities.animal import Animal
from overrides import override

from model.entities.fish import Fish
from model.entities.tree import Tree

from model.terrains.land import Land
from model.terrains.sand import Sand

from constants import HUMAN_TEXTURE_PATH


class Human(Animal):
    count = 0

    def __init__(self):
        super().__init__()
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
    @override
    def getPreys() -> set[type]:
        return {Fish, Tree}
  
    def __str__(self):
        return 'H'
  