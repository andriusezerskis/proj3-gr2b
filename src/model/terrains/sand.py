from overrides import override
from model.terrains.tile import Tile
from model.entities.entity import Entity

from constants import SAND_TEXTURE_PATH


class Sand(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return SAND_TEXTURE_PATH

    def __init__(self, entity: Entity = None) -> None:
        super().__init__(entity)

    def __repr__(self):
        return f"Sand({self.index})"

    def __str__(self):
        return "S"
