"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from copy import copy
from overrides import override

from model.action import Action
from utils import Point

from model.entities.entity import Entity
from model.entities.animal import Animal
from model.terrains.tile import Tile


class Player(Entity):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.claimed_entity: Entity | None = None
        self.health = 0

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
        if (self.getGrid().isInGrid(wantedPosition)
                and not self.getGrid().getTile(wantedPosition).hasEntity()
                and self.isValidTileType(type(self.getGrid().getTile(wantedPosition)))):
            self.getGrid().getTile(oldPosition).removeEntity()
            self.getGrid().getTile(wantedPosition).setEntity(self)
            self.pos = wantedPosition
            return True
        return False

    def getTexturePath(self) -> str:
        return self.claimed_entity.getTexturePath()

    def isValidTileType(self, tileType: type):
        return self.claimed_entity.isValidTileType(tileType)

    def getPreferredTemperature(self) -> float:
        assert isinstance(self.claimed_entity, Animal)
        return self.claimed_entity.getPreferredTemperature()

    @override
    def chooseAction(self) -> Action:
        return Action.IDLE

    def reproduce(self, other: Entity | None) -> None:
        return None
