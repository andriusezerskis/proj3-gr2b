from model.entities.plant import Plant
from overrides import override
from random import random

from utils import Point

from model.terrains.land import Land

from constants import TREE_TEXTURE_PATH, PREFERRED_TEMPERATURE_TREE


class Tree(Plant):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Tree.count += 1

    def __del__(self):
        super().__del__()
        Tree.count -= 1

    @staticmethod
    @override
    def getTexturePath() -> str:
        return TREE_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Land}

    @staticmethod
    def getPreferredTemperature() -> float:
        return PREFERRED_TEMPERATURE_TREE

    def __str__(self):
        return 'T'

