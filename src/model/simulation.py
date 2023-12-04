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

    def step(self) -> Set[Tile]:
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        modifiedTiles = set()
        for line in self.grid.tiles:
            for tile in line:
                if not tile.getEntity():
                    continue
                for entity in self.grid.entitiesInAdjacentTile(tile.index):
                    if not tile.getEntity():
                        continue
                    modifiedTile = self.interaction(tile, entity)
                    self.evolution(tile)
                    modifiedTiles.add(modifiedTile)
        return modifiedTiles - {None}

    def interaction(self, tile: Tile, otherEntity: Entity) -> Tile | None:
        modifiedTile = None
        entity = tile.getEntity()

        if type(entity) is type(otherEntity):
            modifiedTile = self.reproduce(tile)

        elif isinstance(otherEntity, Animal):
            if type(entity) in otherEntity.generateLocalPreys():
                # other_entity.eat()
                modifiedTile = self.dead(tile)
        return modifiedTile

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
            return noEntity[x]

    def moveEntity(self, tile: Tile):
        entity = tile.getEntity()
        noEntity = self.grid.randomTileWithoutEntity(tile)
        if noEntity:
            x = random.randint(0, len(noEntity) - 1)
            noEntity[x].addEntity(entity)
            tile.removeEntity()

    @staticmethod
    def dead(tile: Tile) -> Tile:
        tile.removeEntity()
        return tile

    def getGrid(self) -> Grid:
        return self.grid
