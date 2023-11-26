from plant import Plant
from overrides import override

from constants import TREE_TEXTURE_PATH


class Tree(Plant):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return TREE_TEXTURE_PATH

    @staticmethod
    @override
    def getTexturePath() -> str:
        return

    def __init__(self):
        super().__init__()
