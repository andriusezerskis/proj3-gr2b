import time
from abc import ABC, abstractmethod
from typing import Tuple, List, Set

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from constants import STEP_TIME

from model.simulation import Simulation
from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity


class Window(QMainWindow):
    def __init__(self, grid_size: Tuple[int, int], simulation: Simulation):
        super().__init__()
        self.setWindowTitle('Simulation 2D')
        self.setGeometry(100, 100, 400, 400)
        self.view = GraphicalGrid(grid_size, simulation.getGrid())
        self.setCentralWidget(self.view)
        self.simulation = simulation
        self.timer = QTimer()
        self.timer.setInterval(STEP_TIME)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def recurring_timer(self):
        self.simulation.step()
        self.updateGrid()

    def getGraphicalGrid(self):
        return self.view

    def updateGrid(self):
        start = time.time()
        self.view.updateGrid(self.simulation.getUpdatedTiles())
        print(f"update time : {time.time() - start}")


class GraphicalGrid(QGraphicsView):
    def __init__(self, grid_size: Tuple[int, int], grid: Grid):
        #super().__init__(*__args)
        self.scene = QGraphicsScene()
        super().__init__(self.scene)

        """self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)"""
        self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.zoom_step = 0.1

        self.size = 2048, 2048
        self.grid_size = grid_size
        self.pixmap_items: List[List[List[None | QGraphicsPixmapItem]]] = \
            [[[None, None] for _ in range(grid_size[0])] for _ in range(grid_size[1])]
        self.pixmap_from_path = {}

        start_time = time.time()
        self.drawGrid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        self.scale(0.002, 0.002)

    def updateGrid(self, updated_tiles: Set[Tile]):
        #print(updated_tiles)
        for tile in updated_tiles:
            self._drawEntities(tile)

    def drawGrid(self, grid: Grid):
        for tile in grid:
            self._drawTiles(tile)

    def _drawTiles(self, tile):
        self._drawTerrains(tile)
        self._drawEntities(tile)

    def _drawTerrains(self, tile):
        self._drawPixmap(tile.getIndex(), tile)

    def _drawEntities(self, tile):
        self._drawPixmap(tile.getIndex(), tile.getEntity())

    def _drawPixmap(self, index: Tuple[int, int], item: Tile | Entity):
        i, j = index
        k = 0 if isinstance(item, Tile) else 1
        if self.pixmap_items[i][j][k]:
            self.scene.removeItem(self.pixmap_items[i][j][k])
            #self.pixmap_items[i][j][k].hide()
            #self.pixmap_items[i][j][k].setParentItem(None)
            self.pixmap_items[i][j][k] = None
        if item:
            pixmap_item = QGraphicsPixmapItem(self.getPixmap(item))
            pixmap_item.setPos(j * self.size[0], i * self.size[1])
            self.pixmap_items[i][j][k] = pixmap_item
            self.scene.addItem(pixmap_item)

    def getPixmap(self, tile):
        if tile.getTexturePath() not in self.pixmap_from_path:
            pixmap = QPixmap(tile.getTexturePath())
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmap_from_path[tile.getTexturePath()] = pixmap
            return pixmap
        return self.pixmap_from_path[tile.getTexturePath()]

    def wheelEvent(self, event):
        # Récupérer le facteur de zoom actuel
        zoom_out = event.angleDelta().y() < 0
        zoom_factor = 1.1 if zoom_out else 0.9

        # Appliquer le zoom
        self.zoom_factor *= zoom_factor
        self.scale(zoom_factor, zoom_factor)
