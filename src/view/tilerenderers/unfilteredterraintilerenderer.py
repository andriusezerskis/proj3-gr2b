from PyQt6.QtWidgets import QGraphicsPixmapItem

from model.terrains.tile import Tile
from utils import Point
from view.tilerenderers.tilerenderer import TileRenderer
from overrides import override
from view.pixmaputils import PixmapUtils


class UnfilteredTerrainTileRenderer(TileRenderer):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.terrainLayer = self.createNewLayer()

    def _updateTerrainLayer(self, tile: Tile):
        self.terrainLayer.setPixmap(
            PixmapUtils.getPixmapFromPath(tile.getTexturePath()))

    @override
    def getAllItems(self) -> list[QGraphicsPixmapItem]:
        return [self.terrainLayer]

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
        return False

    @override
    def update(self, tile: Tile):
        self._updateTerrainLayer(tile)
