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
from model.entities.animal import Animal

from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity
from model.player.player import Player

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation:
    def __init__(self):
        super().__init__()
        self.grid = Grid((GRID_WIDTH, GRID_HEIGHT))

        self.stepCount = 0
        self.modifiedTiles = set()
        self.entities = self.grid.initialize()
        self.player = Player(self.grid)

    def step(self) -> None:
        self.modifiedTiles = set()
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        t = time.time()
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity() and not isinstance(tile.getEntity(), Player):
                    for entity in self.grid.entitiesInAdjacentTile(tile.index):
                        self.interaction(tile, entity)
                if tile.getEntity() and not isinstance(tile.getEntity(), Player):
                    self.evolution(tile)

        print(f"compute time : {time.time() - t}")

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def getNumberEntities(self):
        return self.entities

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
        tileWithNoEntity = self.grid.randomTileWithoutEntity(tile)
        if tileWithNoEntity:
            x = random.randint(0, len(tileWithNoEntity) - 1)
            tileWithNoEntity[x].addEntity(newEntity)
            self.entities[entityType] += 1
            self.modifiedTiles.add(tileWithNoEntity[x])

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
        self.entities[type(tile.getEntity())] -= 1
        tile.removeEntity()
        self.modifiedTiles.add(tile)

    def getGrid(self) -> Grid:
        return self.grid

    def getPlayer(self) -> Player:
        return self.player

    def setPlayerEntity(self, tile) -> None:
        self.player.setClaimedEntity(tile)

    def hasPlayer(self) -> bool:
        return self.player.isPlaying()
