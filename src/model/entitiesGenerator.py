import random
from typing import Dict, Type

from model.grid import Grid

from model.entities.algae import Algae
from model.entities.fish import Fish
from model.entities.human import Human
from model.entities.tree import Tree
from model.terrains.land import Land
from model.terrains.tile import Tile
from model.terrains.water import Water


class EntitiesGenerator:

    def generateEntities(self, grid: Grid):
        for tile in grid:
            self.addRandomEntity(tile)

    def addRandomEntity(self, tile: Tile):
        if type(tile) is Water:
            self.generateWaterEntities(tile)
        if type(tile) is Land:
            self.generateLandEntities(tile)

    def generateWaterEntities(self, tile: Tile):
        if random.randint(0, 5) == 1:
            tile.addEntity(Fish)

        elif random.randint(0, 5) == 1:
            tile.addEntity(Algae)

    def generateLandEntities(self, tile: Tile):
        if random.randint(0, 5) == 1:
            tile.addEntity(Human)

        elif random.randint(0, 3) == 1:
            tile.addEntity(Tree)
