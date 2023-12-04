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

    def __init__(self, index, entity: Entity=None) -> None:
        super().__init__(index, entity)
        
    @override
    def getPossibleEntities(self):
        return {Human, Plant}
    
    def __repr__(self):
        return f"Land({self.index})"