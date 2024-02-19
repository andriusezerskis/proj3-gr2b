"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import itertools
import random
import time
import os
import sys

import numpy as np

from constants import *
from model.entities.animals import Crab
from utils import Point
from math import cos, pi

from model.entities.animal import Animal
from model.grid import Grid
from model.generator.gridGenerator import GridGenerator
from model.generator.entitiesGenerator import EntitiesGenerator
from model.terrains.tile import Tile
from model.terrains.tiles import Water
from model.entities.entity import Entity
from model.entities.human import Human
from model.pathfinder import Pathfinder
from model.player.player import Player
from model.renderMonitor import RenderMonitor
from model.action import Action


sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation:
    def __init__(self, size: tuple[int, int]):
        super().__init__()
        self.grid = GridGenerator(Point(size[0], size[1]),
                                  [2, 3, 4, 5, 6],
                                  350).generateGrid()
        EntitiesGenerator().generateEntities(self.grid)

        self.stepCount = 0
        self.modifiedTiles: set[Tile] = set()
        self.updatedEntities: set[Entity] = set()
        self.player = Player(Point(-1, -1))
        self.renderMonitor = RenderMonitor(
            Point(size[0], size[1]), Point(size[0], size[1]))

        self.water_level = Water.getLevel()

        Entity.setGrid(self.grid)

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

    def bordinatorExecution(self, zone,  rayon, cata, pos):
        """
        BORDINATOR EXECUTION
        """
        # if zone == "Ile":
        #     self.grid.islands[0].bordinatorExecution(
        #         zone, rayon, cata, pos, "bordinator")
        if zone == "Rayon":
            for i in self.grid.getTilesInRadius(pos, rayon):
                i.setEntity(Crab(i.getPos()))
                print("ok")

        print(zone, rayon, cata, pos, "bordinator")

    def getTilesInRadius(self, pos: Point, radius: int):
        """
        Return the tiles in the radius of the given position
        """
        r = 2
        neighbor_coords = []
        for j in list(itertools.product(range(-r, r+1), repeat=2)):
            if any(j) and np.sqrt(j[0]**2 + j[1]**2) <= r:
                neighbor_coords.append(j)

        for i in neighbor_coords:
            i = Point(i[0] + pos.x(), i[1] + pos.y())
            if not (0 <= i.x() < self.grid.getSize().x() and 0 <= i.y() < self.grid.getSize().y()):
                neighbor_coords.remove(i)
            yield self.grid.getTile(i)

    def step(self) -> None:
        self.modifiedTiles = set()
        self.updatedEntities = set()
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        t = time.time()
        self.updateWaterLevel()

        for tile in self.grid:
            entity = tile.getEntity()
            if entity and not isinstance(entity, Player) and entity not in self.updatedEntities:
                self.evolution(entity)
                self.updatedEntities.add(entity)

        print(f"compute time : {time.time() - t}")

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def updateWaterLevel(self) -> None:
        # two oscillations a day
        self.water_level = (Water.getLevel() +
                            (-cos(4 * pi * self.stepCount / DAY_DURATION) + 1)
                            * (MAX_WATER_LEVEL - Water.getLevel()) / 2)
        modified = self.grid.updateTilesWithWaterLevel(self.water_level)
        self.modifiedTiles |= modified

    def evolution(self, entity: Entity) -> None:
        entity.evolve()

        if entity.isDead():
            self.dead(self.grid.getTile(entity.getPos()))
            return

        chosenAction = entity.chooseAction()

        match chosenAction:
            case Action.EAT:
                self.eat(entity)
            case Action.MOVE:
                self.moveEntity(entity)
            case Action.REPRODUCE:
                self.reproduceEntity(entity)

    def eat(self, entity: Entity):
        assert isinstance(entity, Animal)
        prey = entity.choosePrey()
        entity.eat(prey)
        self.addModifiedTiles(self.getEntityTile(prey))

    def reproduceEntity(self, entity: Entity):
        mate = None
        if isinstance(entity, Animal):
            mate = entity.getMate()
            # the mate has done an action this timestep
            self.updatedEntities.add(mate)
        newBornTile = entity.reproduce(mate)
        self.addModifiedTiles(newBornTile)

    def moveEntity(self, entity: Entity) -> None:
        movement = entity.chooseMove()

        self.addModifiedTiles(self.getEntityTile(entity))
        entity.move(movement)
        self.addModifiedTiles(self.getEntityTile(entity))

    def dead(self, tile: Tile) -> None:
        tile.removeEntity()
        self.addModifiedTiles(tile)

    def getEntityTile(self, entity: Entity) -> Tile:
        return self.getGrid().getTile(entity.getPos())

    def getGrid(self) -> Grid:
        return self.grid

    def getPlayer(self) -> Player:
        return self.player

    def setPlayerEntity(self, tile) -> None:
        self.player.setClaimedEntity(tile)

    def hasPlayer(self) -> bool:
        return self.player.isPlaying()

    def addModifiedTiles(self, tile: Tile):
        if tile in self.renderMonitor.getRenderingSection():
            self.modifiedTiles.add(tile)

    def getRenderMonitor(self):
        return self.renderMonitor
