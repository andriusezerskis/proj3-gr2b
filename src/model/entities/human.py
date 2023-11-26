from model.entities.animal import Animal
from overrides import override

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
