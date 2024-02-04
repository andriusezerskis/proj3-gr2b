from model.entities.plant import Plant
from overrides import override
from random import random

from model.terrains.land import Land

from constants import TREE_TEXTURE_PATH


class Tree(Plant):
    count = 0

    def __init__(self):
        super().__init__()
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

    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'T'

