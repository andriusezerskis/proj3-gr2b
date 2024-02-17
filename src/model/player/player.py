from copy import copy
from typing import Tuple

from model.action import Action
from utils import Point

from model.entities.entity import Entity
from model.terrains.tile import Tile
from model.grid import Grid

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
                and type(self.getGrid().getTile(wanted_position)) in self.getValidTiles()):
            self.getGrid().getTile(old_position).removeEntity()
            self.getGrid().getTile(wanted_position).setEntity(self)
            self.pos = wanted_position
            return True
        return False

    def getTexturePath(self) -> str:
        return self.claimed_entity.getTexturePath()

    def getValidTiles(self):
        return self.claimed_entity.getValidTiles()

    @override
    def chooseAction(self) -> Action:
        return Action.IDLE

    def reproduce(self) -> None:
        return None
