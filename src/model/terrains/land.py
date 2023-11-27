from overrides import override
from model.terrains.tile import Tile
from model.entities.plant import Plant
from model.entities.human import Human
from model.entities.entity import Entity
from constants import LAND_TEXTURE_PATH


class Land(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return LAND_TEXTURE_PATH

    def __init__(self, entity: Entity=None) -> None:
        super().__init__(entity)
        
    @override
    def getPossibleEntities(self):
        return {Human, Plant}
    
    def getType(self):
        return "land"