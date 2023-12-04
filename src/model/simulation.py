"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import random
import threading
import time
from typing import Set

from constants import *
import os
import sys
from model.entities.algae import Algae
from model.entities.animal import Animal
from model.entities.fish import Fish

from model.grid import Grid
from model.subject import Subject
from model.terrains.tile import Tile
from model.entities.entity import Entity

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation(Subject):
    def __init__(self):
        super().__init__()
        self.grid = Grid((GRID_WIDTH, GRID_HEIGHT))
        self.grid.initialize()
        self.stepCount = 0
        self.modifiedTiles = set()

    def step(self) -> Set[Tile]:
        self.modifiedTiles = set()
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity():
                    self.evolution(tile)
                    for entity in self.grid.entitiesInAdjacentTile(tile.index):
                        self.interaction(tile, entity)

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def interaction(self, tile: Tile, otherEntity: Entity):
        entity = tile.getEntity()

        if type(entity) is type(otherEntity):
            self.reproduce(tile)

        elif isinstance(otherEntity, Animal):
            if type(entity) in otherEntity.generateLocalPreys():
                # other_entity.eat()
                self.dead(tile)

    def evolution(self, tile):
        entity = tile.getEntity()
        if isinstance(entity, Animal):
            self.moveEntity(tile)

        """
        if entity.getType() == "animal":
            entity = Animal(entity)
            if entity.hunger() == 1:
                self.dead(entity)"""

    def reproduce(self, tile: Tile) -> Tile | None:
        entity = tile.getEntity()
        noEntity = self.grid.randomTileWithoutEntity(tile)
        if noEntity:
            x = random.randint(0, len(noEntity) - 1)
            noEntity[x].addEntity(entity)
            self.modifiedTiles.add(noEntity[x])

    def moveEntity(self, tile: Tile):
        entity = tile.getEntity()
        noEntity = self.grid.randomTileWithoutEntity(tile)
        if noEntity:
            x = random.randint(0, len(noEntity) - 1)
            noEntity[x].addEntity(entity)
            self.modifiedTiles.add(noEntity[x])
            tile.removeEntity()
            self.modifiedTiles.add(tile)

    def dead(self, tile: Tile) -> Tile:
        tile.removeEntity()
        self.modifiedTiles.add(tile)

    def getGrid(self) -> Grid:
        return self.grid
