from constants import Disaster
from utils import Point
from model.terrains.tile import Tile
from model.entities.animals import Crab

class DisasterHandler:
    def __init__(self, initialPos: tuple, disasterType: str, radius: int) -> None:
        self.disasterType = disasterType
        self.initialPos = initialPos
        self.radius: int = radius
        self.modifiedTiles = set()
        
    def chooseDisaster(self, tile: Tile):
        initialPosPoint = Point(self.initialPos.x(), self.initialPos.y())
        
        if self.disasterType == Disaster.FIRE_TEXT:
            self.executeFireDisaster(tile, abs(
                    1 - initialPosPoint.manhattanDistance(tile.getPos())/(self.radius*2)))
            
        elif self.disasterType == Disaster.ICE_TEXT:
            self.executeIceDisaster(tile, abs(
                    1 - initialPosPoint.manhattan_distance(tile.getPos())/(self.radius*2)))
            
        elif self.disasterType == Disaster.INVASION_TEXT:
            self.executeCrabDisaster(tile)
        
    def executeFireDisaster(self, tile: Tile, disasterOpacity: float):
        tile.setDisaster(self.disasterType)
        tile.setDisasterOpacity(disasterOpacity)
        
    def executeIceDisaster(self, tile: Tile, disasterOpacity: float):
        tile.setDisaster(self.disasterType)
        tile.setDisasterOpacity(disasterOpacity)
        
    def executeCrabDisaster(self, tile: Tile):
        tile.setEntity(Crab(tile.getPos()))
    
        