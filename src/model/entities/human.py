from animal import Animal
from overrides import override

from fish import Fish
from tree import Tree


class Human(Animal):

    @staticmethod
    @override
    def getClassPreys() -> list:
        return [(Fish, 0.5), (Tree, 0.4)]

    def __init__(self):
        super().__init__()
