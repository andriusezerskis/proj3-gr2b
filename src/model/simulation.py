"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import random
import threading
import time
from typing import List, Set

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
from model.terrains.water import Water

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation(Subject):
    def __init__(self):
        super().__init__()
        self.grid = Grid((GRID_WIDTH, GRID_HEIGHT))
        self.grid.initialize()

        self.step_count = 0

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
        self.step_count += 1
        print("Step " + str(self.step_count))
        self.print_grid()
        modified_tiles = set()
        for line in self.grid.tiles:
            for tile in line:
                if not tile.getEntity():
                    continue
                for entity in self.grid.entitiesInAdjacentTile(tile.index):
                    if not tile.getEntity():
                        continue
                    modified_tile = self.interaction(tile, entity)
                    modified_tiles.add(modified_tile)
        return modified_tiles - {None}

    def interaction(self, tile: Tile, other_entity: Entity) -> Tile | None:
        modified_tile = None
        entity = tile.getEntity()
        if type(entity) is type(other_entity):
            modified_tile = self.reproduce(tile)

        elif isinstance(other_entity, Animal):
            if type(entity) in other_entity.generateLocalPreys():
                # other_entity.eat()
                modified_tile = self.dead(tile)
        return modified_tile

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
        no_entity = self.randomTileWithoutEntity(tile)
        if no_entity:
            x = random.randint(0, len(no_entity) - 1)
            no_entity[x].addEntity(entity)
            return no_entity[x]

    @staticmethod
    def dead(tile: Tile) -> Tile:
        tile.removeEntity()
        return tile

    # TO TEST

    def print_grid(self):
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

    def get_grid(self) -> Grid:
        return self.grid
