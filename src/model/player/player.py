"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from copy import copy

from model.action import Action
from utils import Point

from model.entities.entity import Entity
from model.entities.animal import Animal
from model.terrains.tile import Tile

from overrides import override


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
        old_position = copy(self.pos)
        wanted_position = self.pos + movement
        if (self.getGrid().isInGrid(wanted_position)
                and not self.getGrid().getTile(wanted_position).hasEntity()
                and self.isValidTileType(type(self.getGrid().getTile(wanted_position)))):
            self.getGrid().getTile(old_position).removeEntity()
            self.getGrid().getTile(wanted_position).setEntity(self)
            self.pos = wanted_position
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
