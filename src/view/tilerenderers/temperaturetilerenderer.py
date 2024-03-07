from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsPixmapItem
from overrides import override

from model.terrains.tile import Tile
from view.pixmaputils import PixmapUtils

from parameters import TerrainParameters

from view.tilerenderers.tilerenderer import TileRenderer
from utils import Point


class TemperatureTileRenderer(TileRenderer):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.temperatureLayer = self.createNewLayer()
        self.minTemp = (TerrainParameters.AVERAGE_TEMPERATURE - TerrainParameters.MAX_TEMPERATURE_DIFFERENCE -
                        TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2)
        self.maxTemp = (TerrainParameters.AVERAGE_TEMPERATURE + TerrainParameters.MAX_TEMPERATURE_DIFFERENCE +
                        TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2)

    def _updateTemperatureLayer(self, tile: Tile):
        temperature = tile.getTemperature()

        p = 255 / (-self.maxTemp / self.minTemp + 1)
        m = -p / self.minTemp
        red = int(m * temperature + p)

        hexColor = QColor(red, 0, 255 - red).name()

        self.temperatureLayer.setPixmap(PixmapUtils.getPixmapFromRGBHex(hexColor))

    @override
    def getAllItems(self) -> list[QGraphicsPixmapItem]:
        return [self.temperatureLayer]

    @classmethod
    @override
    def allowsNightCycle(cls) -> bool:
        return False

    @classmethod
    @override
    def mustBeUpdatedAtEveryStep(cls) -> bool:
        return True

    @classmethod
    @override
    def mustNotBeUpdated(cls) -> bool:
        return False

    def update(self, tile: Tile):
        self._updateTemperatureLayer(tile)

