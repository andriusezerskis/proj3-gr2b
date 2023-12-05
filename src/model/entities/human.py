from model.entities.animal import Animal
from overrides import override
from random import random

from model.entities.fish import Fish
from model.entities.tree import Tree

from constants import HUMAN_TEXTURE_PATH


class Human(Animal):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return HUMAN_TEXTURE_PATH

    @staticmethod
    @override
    def getClassPreys() -> list:
        return [(Fish, 0.5), (Tree, 0.4)]

    def __init__(self):
        super().__init__()

    @override
    def reproduce(self) -> None:
        kidsProbability = [(0, 0.1), (1, 0.4), (2, 0.5), (3, 0.1)]
        return random.choices(kidsProbability, weights=[prob for _, prob in kidsProbability])[0]

    def __str__(self):
        return 'H'