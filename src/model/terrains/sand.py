from overrides import override
from model.terrains.tile import Tile
from model.entities.entity import Entity

from constants import SAND_TEXTURE_PATH


class Sand(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return SAND_TEXTURE_PATH

    def __repr__(self):
        return f"Sand({self.pos})"

    def __str__(self):
        return "S"
