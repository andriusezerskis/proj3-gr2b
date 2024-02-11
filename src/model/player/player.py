from typing import Tuple

from utils import Point

from model.entities.entity import Entity
from model.terrains.tile import Tile
from model.grid import Grid


class Player(Entity):

    def __init__(self, grid):
        super().__init__()
        self.claimed_entity: Entity | None = None
        self.grid: Grid = grid
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
        tile.addEntity(self)

    def move(self, movement: Tuple[int, int]):
        old_position = Point(self.position[0], self.position[1])
        wanted_position = Point(self.position[0] + movement[0], self.position[1] + movement[1])
        if (self.grid.isInGrid(wanted_position)
                and not self.grid.getTile(wanted_position).hasEntity()
                and type(self.grid.getTile(wanted_position)) in self.getValidTiles()):
            self.grid.getTile(old_position).removeEntity()
            self.grid.getTile(wanted_position).addEntity(self)
            self.position = wanted_position.x(), wanted_position.y()
            #TODO check if good
            return True
        return False

    def getTexturePath(self) -> str:
        return self.claimed_entity.getTexturePath()

    def getValidTiles(self):
        return self.claimed_entity.getValidTiles()

    @staticmethod
    def reproduce() -> None:
        return None
