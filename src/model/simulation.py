"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import random
import threading
import time
from constants import *
import os
import sys
from model.entities.algae import Algae
from model.entities.animal import Animal
from model.entities.fish import Fish

from model.grid import Grid
from model.subject import Subject

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation(Subject):
    def __init__(self):
        super().__init__()
        self.grid = Grid((GRID_WIDTH, GRID_HEIGHT))
        self.grid.initialize()
        self.generateEntities()
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
        self.notify()
        self.step()
        threading.Timer(STEP_TIME, self.simulate).start()

    def step(self):
        self.step_count += 1
        print("Step " + str(self.step_count))
        self.print_grid()
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity():
                    entities = self.grid.entitiesInAdjacentTile(tile.index)
                    for entity in entities:
                        if tile.getEntity():
                            self.interaction(tile, entity)

    def interaction(self, tile, other_entity):
        entity = tile.getEntity()
        if entity.getType() == other_entity.getType():
            self.reproduce(tile)

        elif isinstance(other_entity, Animal):
            if entity.getType() in other_entity.generateLocalPreys():
                # other_entity.eat()
                self.dead(tile)

    # TO ADD INTO each entity
    """
    def evolution(self, entity):
        if entity.getType() == "animal":
            entity = Animal(entity)
            if entity.hunger() == 1:
                self.dead(entity)"""

    # TO MOVE INTO GRID

    def randomTileWithoutEntity(self, currentTile):
        adjacent_tiles = [
            (currentTile[0] - 1, currentTile[1]),  # up
            (currentTile[0] + 1, currentTile[1]),  # down
            (currentTile[0], currentTile[1] - 1),  # left
            (currentTile[0], currentTile[1] + 1),  # right
            (currentTile[0] - 1, currentTile[1] - 1),  # upper left
            (currentTile[0] - 1, currentTile[1] + 1),  # upper right
            (currentTile[0] + 1, currentTile[1] - 1),  # lower left
            (currentTile[0] + 1, currentTile[1] + 1)  # lower right
        ]

        no_entity = []
        for tile in adjacent_tiles:
            if 0 <= tile[0] < self.grid.size[0] and 0 <= tile[1] < self.grid.size[1]:
                if not self.grid.tiles[tile[0]][tile[1]].getEntity():
                    no_entity.append(
                        self.grid.tiles[tile[0]][tile[1]])
        return no_entity

    def reproduce(self, tile):
        entity = tile.getEntity()
        no_entity = self.randomTileWithoutEntity(tile.index)
        if no_entity != []:
            x = random.randint(0, len(no_entity)-1)
            no_entity[x].addEntity(entity)

    def dead(self, tile):
        tile.removeEntity()

    # TO MOVE INTO GENERATE GRID

    def generateEntities(self):
        for line in self.grid.tiles:
            for tile in line:
                self.addRandomEntity(tile)

    # TO MOVE INTO GENERATE GRID

    def addRandomEntity(self, tile):
        if random.randint(0, 10) == 1:
            tile.addEntity(Fish())
        if random.randint(0, 10) == 2:
            tile.addEntity(Algae())
        if random.randint(0, 10) == 3:
            tile.addEntity(Algae())

    # TO TEST

    def print_grid(self):
        for line in self.grid.tiles:
            for tile in line:
                if tile.getEntity():
                    if tile.getEntity().getType() == Fish:
                        print('f', end=' ')
                    if tile.getEntity().getType() == Algae:
                        print('a', end=' ')
                else:
                    print('_', end=' ')
            print()

    def get_grid(self) -> Grid:
        return self.grid
