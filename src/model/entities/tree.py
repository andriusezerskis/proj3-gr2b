from model.entities.plant import Plant
from overrides import override
from random import random

from constants import TREE_TEXTURE_PATH


class Tree(Plant):
    def __init__(self):
        super().__init__()

    @staticmethod
    @override
    def getTexturePath() -> str:
        return TREE_TEXTURE_PATH

