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
    
    def reproduce(self) -> None:
        kidsProbability = [(0, 0.1), (1, 0.4), (2, 0.3), (3, 0.2)]
        return random.choices(kidsProbability, weights=[prob for _, prob in kidsProbability])[0]

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'F'
