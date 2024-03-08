from PyQt6.QtWidgets import QGraphicsPixmapItem

from model.entities.entity import Entity
from model.generator.gridGenerator import GridGenerator
from model.terrains.tile import Tile
from parameters import ViewParameters
from utils import Point
from view.tilerenderers.tilerenderer import TileRenderer
from overrides import override
from view.pixmaputils import PixmapUtils

from model.movable import Movable
from model.player.player import Player


class ClassicTileRenderer(TileRenderer):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self.terrainLayer = self.createNewLayer()
        self.depthLayer = self.createNewLayer()
        self.entityLayer = self.createNewLayer()
        self.disasterLayer = self.createNewLayer()

    def _updateTerrainLayer(self, tile: Tile):
        self.terrainLayer.setPixmap(PixmapUtils.getPixmapFromPath(tile.getTexturePath()))

    def _updateEntityLayer(self, tile: Tile):
        entity = tile.getEntity()
        if entity:
            self.entityLayer.setPixmap(PixmapUtils.getPixmapFromPath(entity.getTexturePath()))
            self.entityLayer.show()
        else:
            self.entityLayer.hide()

    def _updateDepthLayer(self, tile: Tile):
        self.depthLayer.setPixmap(PixmapUtils.getPixmapFromRGBHex(tile.getFilterColor()))

        # linear mapping from 0 <-> X_LEVEL to MAX_FILTER <-> X+1_LEVEL
        levelRange = GridGenerator.getRange(type(tile))
        m = ViewParameters.MAX_TILE_FILTER_OPACITY / \
            (levelRange[1] - levelRange[0])
        p = -levelRange[0] * m
        opacity = m * tile.getHeight() + p

        if not tile.isGradientAscending():
            opacity = ViewParameters.MAX_TILE_FILTER_OPACITY - opacity

        self.depthLayer.setOpacity(opacity)
        self.depthLayer.show()

    def _updateDisasterLayer(self, tile: Tile):
        self.disasterLayer.setOpacity(tile.getDisasterOpacity())
        self.disasterLayer.setPixmap(PixmapUtils.getPixmapFromPath(tile.getDisasterPathName()))

    @override
    def hideEntity(self):
        self.entityLayer.hide()

    @override
    def getAllItems(self) -> list[QGraphicsPixmapItem]:
        return [self.depthLayer, self.disasterLayer, self.entityLayer, self.terrainLayer]

    @classmethod
    @override
    def allowsNightCycle(cls) -> bool:
        return True

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
        self._updateDepthLayer(tile)
        self._updateEntityLayer(tile)
        self._updateDisasterLayer(tile)
