from utils import Point, getFrenchToEnglishTranslation
from model.terrains.tile import Tile
from model.entities.animals import Crab
from model.disaster import Disaster
from model.entities.entity import Entity
from model.entities.plants import *
from model.entities.plant import Plant
from model.entities.animals import *
from model.entities.human import Human


class DisasterHandler:
    def __init__(self, initialPos: tuple, disasterType: str, radius: int, entityChosen: Entity) -> None:
        self.disasterType = disasterType
        self.initialPos = initialPos
        self.radius: int = radius
        self.modifiedTiles = set()
        self.entityChosen = entityChosen

    def chooseDisaster(self, tile: Tile):
        initialPosPoint = Point(self.initialPos.x(), self.initialPos.y())

        if self.disasterType == Disaster.FIRE_TEXT:
            self.executeFireDisaster(tile, abs(
                1 - initialPosPoint.manhattanDistance(tile.getPos()) / (self.radius * 2)))

        elif self.disasterType == Disaster.ICE_TEXT:
            self.executeIceDisaster(tile, abs(
                1 - initialPosPoint.manhattanDistance(tile.getPos()) / (self.radius * 2)))

        elif self.disasterType == Disaster.INVASION_TEXT:
            self.executeEntityDisaster(tile)

    def executeFireDisaster(self, tile: Tile, disasterOpacity: float):
        tile.setDisaster(self.disasterType)
        tile.setDisasterOpacity(disasterOpacity)

    def executeIceDisaster(self, tile: Tile, disasterOpacity: float):
        tile.setDisaster(self.disasterType)
        tile.setDisasterOpacity(disasterOpacity)

    def executeEntityDisaster(self, tile: Tile):
        if not tile.hasEntity():
            tile.setEntity(globals()[self.entityChosen](tile.getPos()))

