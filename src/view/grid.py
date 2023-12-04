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
        self.view.drawGrid(self.simulation.getGrid())


class SimulationObserver:
    def pingUpdate(self, updated_tiles: Set[Tile]):
        print(updated_tiles)
        for tile in updated_tiles:
            self._drawTile(tile)


class GraphicalGrid(QGraphicsView, SimulationObserver):
    def __init__(self, grid_size: Tuple[int, int], grid: Grid):
        self.scene = QGraphicsScene()
        QGraphicsView.__init__(self, self.scene)

        """self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)"""
        self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.zoom_step = 0.1

        self.size = 2048, 2048
        self.grid_size = grid_size
        self.pixmap_items = [[[None, None] for _ in range(
            grid_size[0])] for _ in range(grid_size[1])]
        self.pixmap_from_path = {}

        start_time = time.time()
        self.drawGrid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        self.scale(0.002, 0.002)

    def drawGrid(self, grid: Grid):
        for tile in grid:
            self._drawTile(tile)

    def _drawTile(self, tile):
        i, j = tile.getIndex()
        pixmap_item = QGraphicsPixmapItem(self.getPixmap(tile))
        pixmap_item.setPos(j * self.size[0], i * self.size[1])
        if self.pixmap_items[i][j][0]:
            self.scene.removeItem(self.pixmap_items[i][j][0])
        self.pixmap_items[i][j][0] = pixmap_item
        # pixmap_item.show()
        self.scene.addItem(pixmap_item)
        if tile.hasEntity():
            pixmap_item = QGraphicsPixmapItem(self.getPixmap(tile.entity))
            pixmap_item.setPos(j * self.size[0], i * self.size[1])
            if self.pixmap_items[i][j][1]:
                self.scene.removeItem(self.pixmap_items[i][j][1])
            self.pixmap_items[i][j][1] = pixmap_item
            # pixmap_item.show()
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
