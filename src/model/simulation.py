"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from random import choice, random
import time

from parameters import TerrainParameters

from utils import getTerminalSubclassesOfClass
from math import cos, pi

# do not trust your IDE, we need it for the globals() function

from model.entities.plant import Plant

###

from model.entities.animal import Animal
from model.grid import Grid
from model.generator.gridGenerator import GridGenerator
from model.generator.entitiesGenerator import EntitiesGenerator
from model.terrains.tile import Tile
from model.terrains.tiles import Water
from model.entities.entity import Entity
from model.player.player import Player
from model.renderMonitor import RenderMonitor
from model.action import Action
from model.disasterhandler import DisasterHandler


class Simulation:
    def __init__(self, gridSize):
        super().__init__()
        self.grid = GridGenerator(gridSize,
                                  [2, 3, 4, 5, 6],
                                  350).generateGrid()
        EntitiesGenerator().generateEntities(self.grid)

        self.stepCount = 0
        self.modifiedTiles: set[Tile] = set()
        self.updatedEntities: set[Entity] = set()
        self.player = Player(None, self.grid)
        self.renderMonitor = RenderMonitor(gridSize, gridSize)

        self.waterLevel = Water.getLevel()

        Entity.setGrid(self.grid)

    def bordinatorExecution(self, zone, radius, disaster, entityChosen, pos):
        # if zone == "Ile":
        #     self.grid.islands[0].bordinatorExecution(
        #         zone, radius, disaster, pos, "bordinator")
        disasterHandler = DisasterHandler(pos, disaster, radius)
        if zone == "Rayon":
            modification = set()
            for tile in self.grid.getTilesInRadius(pos, radius):
                disasterHandler.chooseDisaster(tile)
                if tile.getEntity():
                    tile.getEntity().removeHealthPoints()
                modification.add(tile)
            return modification

    def step(self) -> None:
        self.modifiedTiles = set()
        self.updatedEntities = set()
        self.stepCount += 1
        print("Step " + str(self.stepCount))
        t = time.time()
        self.updateWaterLevel()

        for tile in self.grid:
            self.diminishDisaster(tile)
            entity = tile.getEntity()
            if entity and not isinstance(entity, Player) and entity not in self.updatedEntities:
                self.evolution(entity)
                self.updatedEntities.add(entity)
            if not entity:
                self.spontaneousGeneration(tile)

        print(f"compute time : {time.time() - t}")

    def spontaneousGeneration(self, tile: Tile):
        assert not tile.hasEntity()

        probability = 0.05
        for adjacent in self.getGrid().getAdjacentTiles(tile.getPos()):
            if adjacent.hasEntity():
                probability -= 0.02

        if random() >= probability:
            return

        validTypes = []
        for plantType in getTerminalSubclassesOfClass(Plant):
            assert issubclass(plantType, Plant)
            if plantType.isValidTileType(type(tile)):
                validTypes.append(plantType)

        if len(validTypes) > 0:
            tile.addNewEntity(choice(validTypes))
            self.addModifiedTiles(tile)

    def diminishDisaster(self, tile):
        if tile.disasterOpacity > 0:
            tile.disasterOpacity -= 0.1
        else:
            tile.disaster = None

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def updateWaterLevel(self) -> None:
        # two oscillations a day
        self.waterLevel = (Water.getLevel() +
                           (-cos(4 * pi * self.stepCount / TerrainParameters.DAY_DURATION) + 1)
                           * (TerrainParameters.MAX_WATER_LEVEL - Water.getLevel()) / 2)
        modified = self.grid.updateTilesWithWaterLevel(self.waterLevel)
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
            case Action.DIE:
                self.dead(entity.getTile())

    def eat(self, entity: Entity):
        assert isinstance(entity, Animal)
        prey = entity.choosePrey()
        entity.eat(prey)
        self.dead(prey.getTile())

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
        tile.getEntity().kill()
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
