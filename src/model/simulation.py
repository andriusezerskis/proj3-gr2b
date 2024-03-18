"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from random import choice, random
from typing import Type
import time

from parameters import TerrainParameters

from utils import Point, getTerminalSubclassesOfClass
from math import cos, pi

# do not trust your IDE, we need it for the globals() function

from model.entities.plant import Plant

from model.gridloader import GridLoader

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
from model.disasters.disaster import Disaster
from model.disasters.firedisaster import FireDisaster
from model.disasters.icedisaster import IceDisaster
from parameters import ViewText


class Simulation:
    def __init__(self, gridSize: Point, grid):
        super().__init__()
        self.grid = grid
        self.stepCount = 0
        self.modifiedTiles: set[Tile] = set()
        self.updatedEntities: set[Entity] = set()
        self.player = Player(None, self.grid)
        self.renderMonitor = RenderMonitor(gridSize, gridSize)

        self.waterLevel = Water.getLevel()

        Entity.setGrid(self.grid)

    @staticmethod
    def generateGrid(gridSize):
        grid = GridGenerator(gridSize,
                             [2, 3, 4, 5, 6],
                             350).generateGrid()
        EntitiesGenerator().generateEntities(grid)
        return grid

    def bordinatorExecution(self, zone: str, radius: int, disaster: str, entityChosen, initialPos: Point):
        tiles: list[Tile] = []
        disasterType: Type[Disaster] | None = {ViewText.DISASTER_FIRE_TEXT: FireDisaster,
                                               ViewText.DISASTER_ICE_TEXT: IceDisaster,
                                               ViewText.DISASTER_INVASION_TEXT: None}[disaster]

        entityType = None
        for entity in getTerminalSubclassesOfClass(Entity):
            if entity.__name__ == entityChosen:
                entityType = entity
                break

        assert entityType

        if zone == "Rayon":
            tiles = self.grid.getTilesInManhattanCircle(initialPos, radius)
        elif zone == "Ile":
            initialTile = self.grid.getTile(initialPos)
            tiles = self.grid.getIsland(initialTile)

        for tile in tiles:
            if zone == "Rayon":
                strength = abs(1 - initialPos.manhattanDistance(tile.getPos()) / (radius * 2))
            else:
                strength = 1

            if disasterType is not None:
                disasterType.applyDisaster(tile, strength)
            else:
                tile.addNewEntity(entityType)

        return tiles

    def step(self) -> None:
        self.modifiedTiles = set()
        self.updatedEntities = set()
        self.stepCount += 1
        self.getGrid().regionHandler.advanceTime()
        print("Step " + str(self.stepCount))
        t = time.time()
        self.updateWaterLevel()

        for tile in self.grid:
            self.grid.updateTemperature(tile)
            self.handleDisaster(tile)
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
            if plantType.doesGenerateSpontaneously() and plantType.isValidTileType(type(tile)):
                validTypes.append(plantType)

        if len(validTypes) > 0:
            tile.addNewEntity(choice(validTypes))
            self.addModifiedTiles(tile)

    def handleDisaster(self, tile: Tile):
        if not tile.getDisaster():
            return

        entity = tile.getEntity()
        if entity and isinstance(entity, Entity):
            entity.inflictDamage(tile.getDisaster().getDamagePoints())

        if tile.getDisaster().getStrength() > 0:
            tile.getDisaster().decreaseStrength()
            self.addModifiedTiles(tile)
        else:
            tile.removeDisaster()

    def getUpdatedTiles(self):
        return self.modifiedTiles

    def updateWaterLevel(self) -> None:
        # two oscillations a day
        self.waterLevel = (Water.getLevel() +
                           (-cos(4 * pi * self.stepCount /
                            TerrainParameters.DAY_DURATION) + 1)
                           * (TerrainParameters.MAX_WATER_LEVEL - Water.getLevel()) / 2)
        modified = self.grid.updateTilesWithWaterLevel(self.waterLevel)
        self.modifiedTiles |= modified

    def evolution(self, entity: Entity) -> None:
        if entity.evolve():
            self.addModifiedTiles(entity.getTile())

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
        if entity.eat(prey):
            self.dead(prey.getTile())
        else:
            self.addModifiedTiles(prey.getTile())

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
        if tile.hasEntity():
            tile.getEntity().kill()
            tile.removeEntity()
            self.addModifiedTiles(tile)

    def getEntityTile(self, entity: Entity) -> Tile:
        return self.getGrid().getTile(entity.getPos())

    def getGrid(self) -> Grid:
        return self.grid

    def getPlayer(self) -> Player:
        return self.player

    def setPlayerEntity(self, tile: Tile) -> None:
        self.player.setClaimedEntity(tile)

    def hasPlayer(self) -> bool:
        return self.player.isPlaying()

    def addModifiedTiles(self, tile: Tile):
        if tile in self.renderMonitor.getRenderingSection():
            self.modifiedTiles.add(tile)

    def getRenderMonitor(self):
        return self.renderMonitor
