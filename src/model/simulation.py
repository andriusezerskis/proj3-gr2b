"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import random
import time

from constants import *
import os
import sys

from utils import Point
from model.entities.animal import Animal

from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity
from model.entities.human import Human

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation:
    def __init__(self):
        super().__init__()
        self.grid = Grid(Point(GRID_WIDTH, GRID_HEIGHT))

        self.stepCount = 0
        self.modifiedTiles = set()
        self.grid.initialize()

    def step(self) -> None:
        self.modifiedTiles = set()
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        t = time.time()
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity():
                    for entity in self.grid.entitiesInAdjacentTile(tile.getPos()):
                        self.interaction(tile, entity)
                if tile.getEntity():
                    self.evolution(tile)

        print(f"compute time : {time.time() - t}")

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def interaction(self, tile: Tile, otherEntity: Entity):
        entity = tile.getEntity()

        if type(entity) is type(otherEntity) and entity.reproduce() and otherEntity.reproduce():
            self.reproduce(tile)

        elif isinstance(otherEntity, Animal):
            if type(entity) in otherEntity.generateLocalPreys():
                otherEntity.eat()
                self.dead(tile)

    def evolution(self, tile):
        entity = tile.getEntity()
        if entity:
            entity.evolve()
            if entity.isDead():
                self.dead(tile)
            elif isinstance(entity, Animal):
                self.moveEntity(tile)

    def reproduce(self, tile: Tile):
        entityType = type(tile.getEntity())
        newEntity = entityType()
        tileWithNoEntity = self.grid.randomTileWithoutEntity(tile.getPos())
        if tileWithNoEntity:
            x = random.randint(0, len(tileWithNoEntity) - 1)
            tileWithNoEntity[x].addEntity(newEntity)
            self.modifiedTiles.add(tileWithNoEntity[x])

    def moveEntity(self, tile: Tile):
        entity = tile.getEntity()
        noEntity = self.grid.randomTileWithoutEntity(tile.getPos())
        if noEntity:
            x = random.randint(0, len(noEntity) - 1)
            noEntity[x].addEntity(entity)
            self.modifiedTiles.add(noEntity[x])
            tile.removeEntity()
            self.modifiedTiles.add(tile)

    def dead(self, tile: Tile) -> None:
        tile.removeEntity()
        self.modifiedTiles.add(tile)

    def getGrid(self) -> Grid:
        return self.grid
