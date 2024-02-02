from overrides import override
from random import random

from constants import FISH_TEXTURE_PATH

from model.entities.animal import Animal
from model.entities.algae import Algae


class Fish(Animal):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return FISH_TEXTURE_PATH

    @staticmethod
    @override
    def getClassPreys() -> list[tuple]:
        return [(Algae, 0.99)]

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'F'
