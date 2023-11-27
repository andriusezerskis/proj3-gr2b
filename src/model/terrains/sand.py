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

    @override
    def getPossibleEntities(self):
        return {}

    def getType(self):
        return "sand"