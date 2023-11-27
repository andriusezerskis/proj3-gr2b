from overrides import override
from model.terrains.tile import Tile
from model.entities.fish import Fish
from model.entities.algae import Algae
from model.entities.entity import Entity
from constants import WATER_TEXTURE_PATH


class Water(Tile):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return WATER_TEXTURE_PATH

    def __init__(self, index, entity: Entity=None) -> None:
        super().__init__(index, entity)
        
    @override    
    def getPossibleEntities(self):
        return {Fish, Algae} # returns a set so that we can check 
    
    def getType(self):
        return "water"