from overrides import override
from model.terrains.tile import Tile
from model.entities.entity import Entity
from constants import WATER_TEXTURE_PATH


class Water(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return WATER_TEXTURE_PATH

    def __repr__(self):
        return f"Water({self.pos})"

    def __str__(self):
        return "W"
