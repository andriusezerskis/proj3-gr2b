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
        self.position: Tuple[int, int] | None = None
        self.health = 0

    def isPlaying(self):
        return self.claimed_entity is not None

    def getPosition(self):
        return self.position

    def setClaimedEntity(self, tile: Tile):
        self.claimed_entity = tile.getEntity()
        self.position = tile.getIndex()
        tile.removeEntity()
        tile.setEntity(self)

    def move(self, movement: Tuple[int, int]):
        old_position = Point(self.position[1], self.position[0])
        wanted_position = Point(self.position[1] + movement[1], self.position[0] + movement[0])
        if (self.getGrid().isInGrid(wanted_position.y(), wanted_position.x())
                and not self.getGrid().getTile(wanted_position).hasEntity()
                and type(self.getGrid().getTile(wanted_position)) in self.getValidTiles()):
            self.getGrid().getTile(old_position).removeEntity()
            self.getGrid().getTile(wanted_position).setEntity(self)
            self.position = wanted_position.y(), wanted_position.x()
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
