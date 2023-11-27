from model.entities.plant import Plant
from overrides import override

from constants import TREE_TEXTURE_PATH


class Tree(Plant):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return TREE_TEXTURE_PATH

    def __init__(self):
        super().__init__()
