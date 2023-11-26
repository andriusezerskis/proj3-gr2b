from overrides import override

from constants import FISH_TEXTURE_PATH

from animal import Animal
from algae import Algae


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
