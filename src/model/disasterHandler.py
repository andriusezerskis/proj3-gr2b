from utils import Point, getFrenchToEnglishTranslation
from model.terrains.tile import Tile
from model.disaster import Disaster
from model.entities.entity import Entity
from model.entities.plants import *
from model.entities.animals import *
from model.entities.human import Human


class DisasterHandler:
    def __init__(self, initialPos: tuple, disasterType: str, radius: int, entityChosen: Entity) -> None:
        self.disasterType: str = disasterType
        self.initialPos: tuple = initialPos
        self.radius: int = radius
        self.modifiedTiles: set = set()
        self.entityChosen: Entity = entityChosen

    def chooseDisaster(self, tile: Tile, zone: str) -> Tile:
        """Chooses a disaster based on disasterType and whether it's for a radius or an island

        Args:
            tile (Tile): tile on which the disaster is executed
            zone (str): whether the disaster is for a radius or an entire island

        Returns:
            Tile: modified tile after disaster execution
        """
        initialPosPoint = Point(self.initialPos.x(), self.initialPos.y())

        if self.disasterType == Disaster.FIRE_TEXT:
            if zone == "Rayon":
                self.executeFireDisaster(tile, abs(
                    1 - initialPosPoint.manhattanDistance(tile.getPos()) / (self.radius * 2)))
            else:
                self.executeFireDisaster(tile, 1)
            if tile.getEntity():  # if an entity is present, disaster inflicts damage
                tile.getEntity().removeHealthPoints()

        elif self.disasterType == Disaster.ICE_TEXT:
            if zone == "Rayon":
                self.executeIceDisaster(tile, abs(
                    1 - initialPosPoint.manhattanDistance(tile.getPos()) / (self.radius * 2)))
            else:
                self.executeFireDisaster(tile, 1)
            if tile.getEntity():  # if an entity is present, disaster inflicts damage
                tile.getEntity().removeHealthPoints()

        elif self.disasterType == Disaster.INVASION_TEXT:
            self.executeEntityInvasion(tile)
        return tile

    def executeFireDisaster(self, tile: Tile, disasterOpacity: float):
        tile.setDisaster(self.disasterType)
        tile.setDisasterOpacity(disasterOpacity)

    def executeIceDisaster(self, tile: Tile, disasterOpacity: float):
        tile.setDisaster(self.disasterType)
        tile.setDisasterOpacity(disasterOpacity)

    def executeEntityInvasion(self, tile: Tile):
        entityType = globals()[self.entityChosen]
        tile.addNewEntity(entityType)
