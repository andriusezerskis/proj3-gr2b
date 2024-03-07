from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsPixmapItem
from overrides import override

from model.terrains.tile import Tile
from view.pixmaputils import PixmapUtils

from view.tilerenderers.tilerenderer import TileRenderer
from utils import Point


class DepthTileRenderer(TileRenderer):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.depthLayer = self.createNewLayer()

    def _updateDepthLayer(self, tile: Tile):
        height = tile.getHeight()

        intensity = (height + 1) / 2
        hexColor = QColor(int(255 * intensity), int(255 * intensity), int(255 * intensity)).name()

        self.depthLayer.setPixmap(PixmapUtils.getPixmapFromRGBHex(hexColor))

    @override
    def getAllItems(self) -> list[QGraphicsPixmapItem]:
        return [self.depthLayer]

    @classmethod
    @override
    def allowsNightCycle(cls) -> bool:
        return False

    @classmethod
    @override
    def mustBeUpdatedAtEveryStep(cls) -> bool:
        return False

    @classmethod
    @override
    def mustNotBeUpdated(cls) -> bool:
        return True

    def update(self, tile: Tile):
        self._updateDepthLayer(tile)

