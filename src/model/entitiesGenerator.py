import random
from model.entities.algae import Algae
from model.entities.fish import Fish
from model.terrains.tile import Tile
from model.terrains.water import Water


class EntitiesGenerator:

    def generateEntities(self, tiles):
        for line in tiles:
            for tile in line:
                self.addRandomEntity(tile)

    def addRandomEntity(self, tile: Tile):
        if type(tile) is Water:
            self.generateWaterEntities(tile)

    def generateWaterEntities(self, tile: Tile):
        # if random.randint(0, 5) == 1:
        # tile.addEntity(Fish())
        if random.randint(0, 2) == 1:
            tile.addEntity(Algae())
