"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
import time
from copy import copy
from overrides import override
from typing import Dict, Type
from overrides import override

from utils import Point, getTerminalSubclassesOfClass

from model.entities.entity import Entity
from model.entities.animal import Animal
from model.terrains.tile import Tile
from model.movable import Movable
from model.crafting.loots import Loot
from view.playerDockView import PlayerDockView

from utils import getNormalizedVector


class Player(Movable):

    def __init__(self, pos: Point | None, grid: "Grid"):
        super().__init__()
        self.pos = pos
        self.grid = grid
        self.claimed_entity: Entity | None = None
        self.inventory = {loot_class.__name__: 0 for loot_class in getTerminalSubclassesOfClass(Loot)}

        self.abilityUnlockedRod = False
        self._isFishing = False
        self.startHookTime = None
        self.hookVelocity = 0
        self.hookDirection = None
        self.targetedTileForHooking = None
        self.hookPlace = None

    def isPlaying(self):
        return self.claimed_entity is not None

    def setClaimedEntity(self, tile: Tile):
        self.claimed_entity = tile.getEntity()
        self.pos = tile.getPos()
        tile.removeEntity()
        tile.setEntity(self)

    def removeClaimedEntity(self, killed=False):
        self._reset(killed)

    def isDead(self):
        """The entity chosen never dies

        Returns:
            _type_: _description_
        """
        return False

    def getTile(self):
        return self.grid.getTile(self.pos)

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

    def isValidTileType(self, tileType: Type[Tile]):
        return self.claimed_entity.isValidTileType(tileType)

    def getPreferredTemperature(self) -> float:
        assert isinstance(self.claimed_entity, Animal)
        return self.claimed_entity.getPreferredTemperature()

    def kill(self):
        PlayerDockView.lageEntity(True)

    def canFish(self):
        return self.abilityUnlockedRod

    def hasEnoughQuantityToCraft(self, item):
        for material, quantity in item.getBlueprint().items():
            if self.inventory.get(material) < quantity:
                return False
        return True

    def craft(self, item):
        if not self.hasEnoughQuantity(item):
            return False
        self.removeFromInventory(item.getBlueprint())

    def isFishing(self):
        return self._isFishing

    def startFishing(self, tile):
        if not self._isFishing:
            self.stopFishing()
            self.targetedTileForHooking = tile
            self._isFishing = True
            self.hookDirection = getNormalizedVector(tile.getPos() - self.pos)
            self.startHookTime = time.time()

    def throwHook(self):
        self.hookVelocity = min(5 * (time.time() - self.startHookTime), 8)
        self.hookPlace = self.pos + (self.hookDirection * self.hookVelocity)
        return self.hookPlace

    def getTargetedTileForHooking(self):
        return self.targetedTileForHooking

    def getHookPlace(self):
        return self.hookPlace

    def stopFishing(self):
        self.hookVelocity = 0
        self.hookDirection = 0
        self.startHookTime = None
        self._isFishing = False
        self.targetedTileForHooking = None
        self.hookPlace = None

    def _reset(self, killed=False):
        if not killed:
            self.claimed_entity.setPos(self.pos)
            self.grid.getTile(self.pos).setEntity(self.claimed_entity)
        else:
            self.claimed_entity.kill()
        self.pos = None
        self.claimed_entity = None
        self.inventory = {loot_class.__name__: 0 for loot_class in getTerminalSubclassesOfClass(Loot)}
        self.abilityUnlockedRod = False
        self.stopFishing()
