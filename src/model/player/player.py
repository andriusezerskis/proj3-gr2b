from typing import Tuple

from model.entities.entity import Entity
from model.terrains.tile import Tile


class Player:
    def __init__(self):
        self.claimed_entity: Entity | None = None
        self.position: Tuple[int, int] | None = None
        self.health = 0

    def setClaimedEntity(self, tile: Tile):
        self.claimed_entity = tile.getEntity()
        self.position = tile.getIndex()
        tile.removeEntity()
        tile.addEntity(self)

    def move(self, movement: Tuple[int, int]):
        self.position = self.position[0] + movement[0], self.position[1] + movement[1]