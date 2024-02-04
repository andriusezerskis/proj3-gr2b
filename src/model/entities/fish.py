from overrides import override
from random import random

from constants import FISH_TEXTURE_PATH

from model.entities.animal import Animal
from model.entities.algae import Algae

from model.terrains.water import Water


class Fish(Animal):
    count = 0

    @staticmethod
    @override
    def getTexturePath() -> str:
        return FISH_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Water}

    @staticmethod
    @override
    def getClassPreys() -> list[tuple]:
        return [(Algae, 0.99)]

    def __init__(self):
        super().__init__()
        Fish.count += 1

    def __del__(self):
        super().__del__()
        Fish.count -= 1

    def __str__(self):
        return 'F'
