from PyQt6.QtGui import QPixmap, QImage, QColor
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

from parameters import ViewParameters

from model.terrains.tile import Tile
from utils import Point

from abc import ABC, abstractmethod


class TileRenderer(ABC):

    _scene: QGraphicsScene = None

    def __init__(self, pos: Point):
        assert self.getScene()
        self.pos = pos
        self.layers: set[QGraphicsPixmapItem] = set()

    @staticmethod
    def setScene(scene: QGraphicsScene):
        TileRenderer._scene = scene

    @staticmethod
    def getScene() -> QGraphicsScene:
        return TileRenderer._scene

    def createNewLayer(self):
        layer = QGraphicsPixmapItem()
        layer.setPos(self.pos.y() * ViewParameters.TEXTURE_SIZE,
                     self.pos.x() * ViewParameters.TEXTURE_SIZE)
        self.getScene().addItem(layer)
        self.layers.add(layer)
        return layer

    def show(self):
        for layer in self.layers:
            layer.show()

    def hide(self):
        for layer in self.layers:
            layer.hide()

    def hideEntity(self):
        return

    @abstractmethod
    def update(self, tile: Tile):
        ...
