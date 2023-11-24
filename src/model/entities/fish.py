from overrides import override

from animal import Animal
from plankton import Plankton


class Fish(Animal):

    @staticmethod
    @override
    def getClassPreys() -> list[tuple]:
        return [(Plankton, 0.99)]

    def __init__(self):
        super().__init__()
