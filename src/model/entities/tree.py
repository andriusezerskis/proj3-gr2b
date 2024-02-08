from model.entities.plant import Plant
from overrides import override
from random import random

from model.terrains.land import Land

from constants import TREE_TEXTURE_PATH


class Tree(Plant):
    def __init__(self):
        super().__init__()

    @staticmethod
    @override
    def getTexturePath() -> str:
        return TREE_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Land}

    def __str__(self):
        return 'T'

