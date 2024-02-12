"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import random
import time
import os
import sys

from constants import *
from utils import Point
from math import cos, pi

from model.entities.animal import Animal
from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity
from model.entities.human import Human
from model.pathfinder import Pathfinder
from model.player.player import Player
from model.renderMonitor import RenderMonitor


sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))

class Simulation:
    def __init__(self):
        super().__init__()
        self.grid = Grid(Point(GRID_WIDTH, GRID_HEIGHT))

        self.stepCount = 0
        self.modifiedTiles: set[Tile] = set()
        self.entities = self.grid.initialize()
        self.player = Player(self.grid)
        self.renderMonitor = RenderMonitor()

        self.water_level = WATER_LEVEL

        # self._TEST_PATHFINDING()

    def _TEST_PATHFINDING(self):
        """
        PATHFINDING TEST, TO REMOVE
        """
        for tile in self.grid.islands[0]:
            if type(tile.getEntity()) is Human:
                pathfinder = Pathfinder(self.grid)
                current = tile.getPos()
                dest = random.choice(list(self.grid.islands[0])).getPos()
                t1 = time.time()
                if pathfinder.findPath(tile.getEntity(), current, dest):
                    print(
                        f"Found path from {current} to {dest} in {time.time() - t1}s")
                    print("simulating path...")
                    for move in pathfinder.getPath():
                        print(
                            f"{current} + {move} = {current + move} (tile {self.grid.getTile(current + move)})")
                        current = current + move
                break

    def step(self) -> None:
        self.modifiedTiles = set()
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        t = time.time()
        self.updateWaterLevel()
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity() and not isinstance(tile.getEntity(), Player):
                    for entity in self.grid.entitiesInAdjacentTile(tile.getPos()):
                        self.interaction(tile, entity)
                if tile.getEntity() and not isinstance(tile.getEntity(), Player):
                    self.evolution(tile)

        print(f"compute time : {time.time() - t}")

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def getNumberEntities(self):
        return self.entities

    def updateWaterLevel(self) -> None:
        self.water_level = (WATER_LEVEL +
                            (-cos(2 * pi * self.stepCount / DAY_DURATION) + 1) * (MAX_WATER_LEVEL - WATER_LEVEL) / 2)
        modified = self.grid.updateTilesWithWaterLevel(self.water_level)
        self.modifiedTiles |= modified

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
            self.addModifiedTiles(noEntity[x])
            tile.removeEntity()
            self.addModifiedTiles(tile)

    def dead(self, tile: Tile) -> None:
        tile.removeEntity()
        self.addModifiedTiles(tile)

    def getGrid(self) -> Grid:
        return self.grid

    def getPlayer(self) -> Player:
        return self.player

    def setPlayerEntity(self, tile) -> None:
        self.player.setClaimedEntity(tile)

    def hasPlayer(self) -> bool:
        return self.player.isPlaying()

    def addModifiedTiles(self, tile):
        if tile in self.renderMonitor.getRenderingSection():
            self.modifiedTiles.add(tile)

    def getRenderMonitor(self):
        return self.renderMonitor
