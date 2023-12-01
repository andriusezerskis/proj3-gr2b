from model.entities.plant import Plant
from overrides import override
from random import random

from constants import TREE_TEXTURE_PATH


class Tree(Plant):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return TREE_TEXTURE_PATH

    def __init__(self):
        super().__init__()

    @override
    def reproduce(self) -> None:
        kidsProbability = [(0, 0.1), (1, 0.4), (2, 0.3), (3, 0.2)]
        return random.choices(kidsProbability, weights=[prob for _, prob in kidsProbability])[0]