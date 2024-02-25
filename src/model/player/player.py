"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from copy import copy
from utils import Point

from model.entities.entity import Entity
from model.entities.animal import Animal
from model.terrains.tile import Tile
from model.grid import Grid


class Player:

    def __init__(self, pos: Point, grid: Grid):
        self.pos = pos
        self.grid = grid
        self.claimed_entity: Entity | None = None

    def isPlaying(self):
        return self.claimed_entity is not None

    def setClaimedEntity(self, tile: Tile):
        self.claimed_entity = tile.getEntity()
        self.pos = tile.getPos()
        tile.removeEntity()
        tile.setEntity(self)

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

    def getPos(self):
        return self.pos

    def getTexturePath(self) -> str:
        print(self.claimed_entity.getTexturePath())
        return self.claimed_entity.getTexturePath()

    def isValidTileType(self, tileType: type):
        return self.claimed_entity.isValidTileType(tileType)

    def getPreferredTemperature(self) -> float:
        assert isinstance(self.claimed_entity, Animal)
        return self.claimed_entity.getPreferredTemperature()