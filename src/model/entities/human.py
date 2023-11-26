from model.entities.animal import Animal
from overrides import override

from model.entities.fish import Fish
from model.entities.tree import Tree


class Human(Animal):

    @staticmethod
    @override
    def getClassPreys() -> list:
        return [(Fish, 0.5), (Tree, 0.4)]

    def __init__(self):
        super().__init__()
