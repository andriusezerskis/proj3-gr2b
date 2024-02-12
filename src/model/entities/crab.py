from overrides import override

from constants import CRAB_TEXTURE_PATH

from model.entities.animal import Animal
from model.terrains.water import Water
from model.terrains.sand import Sand
from model.entities.algae import Algae
from model.entities.fish import Fish


class Crab(Animal):
    count = 0
    
    def __init__(self):
        super().__init__()
        Crab.count += 1

    def __del__(self):
        super().__del__()
        Crab.count -= 1

    @staticmethod
    @override
    def getTexturePath() -> str:
        return CRAB_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Sand, Water}

    @staticmethod
    @override
    def getClassPreys() -> list[tuple]:
        return [(Algae, 0.4), (Fish, 0.6)]