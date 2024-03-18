from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsPixmapItem
from overrides import override

from model.terrains.tile import Tile
from view.pixmaputils import PixmapUtils

from parameters import TerrainParameters

from view.tilerenderers.tilerenderer import TileRenderer
from utils import Point


class TemperatureTileRenderer(TileRenderer):

    minTemp = None
    maxTemp = None
    _p = None
    _m = None

    def __init__(self, pos: Point):
        super().__init__(pos)
        if not self.minTemp:
            self._initConstants()
        self.temperatureLayer = self.createNewLayer()

    def _initConstants(self):
        self.minTemp = (TerrainParameters.AVERAGE_TEMPERATURE - TerrainParameters.MAX_TEMPERATURE_DIFFERENCE -
                        TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2)
        self.maxTemp = (TerrainParameters.AVERAGE_TEMPERATURE + TerrainParameters.MAX_TEMPERATURE_DIFFERENCE +
                        TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2)
        self._p = 255 / (-self.maxTemp / self.minTemp + 1)
        self._m = -self._p / self.minTemp

    def _getColor(self, temperature: float):
        return max(0, min(255, int(self._m * temperature + self._p)))

    def _updateTemperatureLayer(self, tile: Tile):
        temperature = tile.getTemperature()

        red = self._getColor(temperature)

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

