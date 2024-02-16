from overrides import override
from random import random

from constants import FISH_TEXTURE_PATH, PREFERRED_TEMPERATURE_FISH

from utils import Point

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
    def getPreferredTemperature() -> float:
        return PREFERRED_TEMPERATURE_FISH

    @staticmethod
    @override
    def getPreys() -> set[type]:
        return {Algae}

    def __init__(self, pos: Point):
        super().__init__(pos)
        Fish.count += 1

    def __del__(self):
        super().__del__()
        Fish.count -= 1

    def __str__(self):
        return 'F'
