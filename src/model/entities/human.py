from model.entities.animal import Animal
from overrides import override
from random import random

from model.entities.fish import Fish
from model.entities.tree import Tree

from model.terrains.land import Land
from model.terrains.sand import Sand

from constants import HUMAN_TEXTURE_PATH


class Human(Animal):
    def __init__(self):
        super().__init__()

        
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
    def getClassPreys() -> list:
        return [(Fish, 0.5), (Tree, 0.4)]
  
    def __str__(self):
        return 'H'
  