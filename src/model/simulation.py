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

    def run(self):
        print("Starting simulation in 5s...")
        """end = 0
        start = time.time()
        while True:
            end = time.time()
            if (end-start) > STEP_TIME:
                self.notify()
                self.step()
                start = time.time()"""
        threading.Timer(5.0, self.simulate).start()

    def simulate(self):
        self.notify(self.step())
        threading.Timer(STEP_TIME, self.simulate).start()

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

    # TO ADD INTO each entity
    """
    def evolution(self, entity):
        if entity.getType() == "animal":
            entity = Animal(entity)
            if entity.hunger() == 1:
                self.dead(entity)"""

    # TO MOVE INTO GRID

    def randomTileWithoutEntity(self, currentTile):
        """Generate random tile to reproduce, it must be empty and must be the same tile type as the currentTile
        """
        adjacent_tiles = [
            (currentTile.index[0] - 1, currentTile.index[1]),  # up
            (currentTile.index[0] + 1, currentTile.index[1]),  # down
            (currentTile.index[0], currentTile.index[1] - 1),  # left
            (currentTile.index[0], currentTile.index[1] + 1),  # right
            (currentTile.index[0] - 1, currentTile.index[1] - 1),  # upper left
            (currentTile.index[0] - 1,
             currentTile.index[1] + 1),  # upper right
            (currentTile.index[0] + 1, currentTile.index[1] - 1),  # lower left
            (currentTile.index[0] + 1, currentTile.index[1] + 1)  # lower right
        ]

        no_entity = []
        for tile in adjacent_tiles:
            if 0 <= tile[0] < self.grid.size[0] and 0 <= tile[1] < self.grid.size[1]:
                randomTile = self.grid.tiles[tile[0]][tile[1]]
                if not randomTile.getEntity():
                    if (type(currentTile) == type(randomTile)):
                        no_entity.append(
                            self.grid.tiles[tile[0]][tile[1]])
        return no_entity

    def reproduce(self, tile: Tile) -> Tile | None:
        entity = tile.getEntity()
        noEntity = self.randomTileWithoutEntity(tile)
        if noEntity:
            x = random.randint(0, len(noEntity) - 1)
            noEntity[x].addEntity(entity)
            return noEntity[x]

    @staticmethod
    def dead(tile: Tile) -> Tile:
        tile.removeEntity()
        return tile

    # TO TEST

    def printGrid(self):
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity():
                    if type(tile.getEntity()) == Fish:
                        print('f', end=' ')
                    if type(tile.getEntity()) == Algae:
                        print('a', end=' ')
                else:
                    print('_', end=' ')
            print()

    def getGrid(self) -> Grid:
        return self.grid
