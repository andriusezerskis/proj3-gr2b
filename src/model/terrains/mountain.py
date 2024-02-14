from overrides import override
from model.terrains.tile import Tile

from constants import MOUNTAIN_TEXTURE_PATH


class Mountain(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return MOUNTAIN_TEXTURE_PATH

    def __repr__(self):
        return f"Mountain({self.pos})"

    def __str__(self):
        return "M"
