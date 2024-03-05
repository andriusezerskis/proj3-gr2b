"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from copy import copy
from overrides import override
from typing import Dict

from utils import Point, getTerminalSubclassesOfClass

from model.entities.entity import Entity
from model.entities.animal import Animal
from model.terrains.tile import Tile
from model.movable import Movable
from model.crafting.loots import Loot


class Player(Movable):

    def __init__(self, pos: Point | None, grid: "Grid"):
        super().__init__()
        self.pos = pos
        self.grid = grid
        self.claimed_entity: Entity | None = None
        self.inventory = {
            loot_class.__name__: 0 for loot_class in getTerminalSubclassesOfClass(Loot)}

    def isPlaying(self):
        return self.claimed_entity is not None

    def setClaimedEntity(self, tile: Tile):
        self.claimed_entity = tile.getEntity()
        self.pos = tile.getPos()
        tile.removeEntity()
        tile.setEntity(self)

    def removeClaimedEntity(self):
        self.claimed_entity.setPos(self.pos)
        self.grid.getTile(self.pos).setEntity(self.claimed_entity)
        self.pos = None
        self.claimed_entity = None

    def move(self, movement: Point):
        oldPosition = copy(self.pos)
        wantedPosition = self.pos + movement
        if (self.grid.isInGrid(wantedPosition)
                and not self.grid.getTile(wantedPosition).hasEntity()
                and self.isValidTileType(type(self.grid.getTile(wantedPosition)))):
            self.grid.getTile(oldPosition).removeEntity()
            self.grid.getTile(wantedPosition).setEntity(self)
            self.pos = wantedPosition
            return True
        return False

    def addInInventory(self, loots: Dict[str, int]):
        for loot_name in loots:
            self.inventory[loot_name] += loots[loot_name]

    def removeFromInventory(self, recipe: Dict[str, int]):
        for loot_name in recipe:
            self.inventory[loot_name] -= recipe[loot_name]

    def getInventory(self):
        return self.inventory

    @override
    def getPos(self) -> Point:
        return self.pos

    def getTexturePath(self) -> str:
        return self.claimed_entity.getTexturePath()

    def isValidTileType(self, tileType: type):
        return self.claimed_entity.isValidTileType(tileType)

    def getPreferredTemperature(self) -> float:
        assert isinstance(self.claimed_entity, Animal)
        return self.claimed_entity.getPreferredTemperature()
