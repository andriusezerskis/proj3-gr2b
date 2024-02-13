from overrides import override
from model.terrains.tile import Tile
from model.entities.entity import Entity

from constants import BOAT_TEXTURE_PATH


class Boat(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return BOAT_TEXTURE_PATH

    def __repr__(self):
        return f"Boat({self.pos})"

    def __str__(self):
        return "S"
