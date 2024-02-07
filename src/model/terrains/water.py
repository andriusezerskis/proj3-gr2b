from overrides import override
from model.terrains.tile import Tile
from model.entities.entity import Entity
from constants import WATER_TEXTURE_PATH


class Water(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return WATER_TEXTURE_PATH

    def __init__(self, index, entity: Entity = None) -> None:
        super().__init__(index, entity)

    def __repr__(self):
        return f"Water({self.index})"

    def __str__(self):
        return "W"
