import time
from typing import Tuple, List

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView

from model.terrains.land import Land
from model.terrains.water import Water
from model.entities.human import Human
from model.entities.tree import Tree
from model.simulation import Simulation
from model.grid import Grid


class Window(QMainWindow):
    def __init__(self, grid_size: Tuple[int, int], simulation: Simulation):
        super().__init__()
        self.setWindowTitle('Simulation 2D')
        self.setGeometry(100, 100, 400, 400)
        self.view = GraphicalGrid(grid_size, simulation.get_grid())
        self.setCentralWidget(self.view)

    def get_graphical_grid(self):
        return self.view

class SimulationObserver:
    def ping_update(self, query):
        print("simulation new step")


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
        self.pixmap_items = [[[None, None] for _ in range(grid_size[0])] for _ in range(grid_size[1])]
        self.pixmap_from_path = {}

        start_time = time.time()
        self.draw_grid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        self.scale(0.002, 0.002)

    def draw_grid(self, grid: Grid):
        for (i, j), tile in grid:
            pixmap_item = QGraphicsPixmapItem(self.get_pixmap(tile))
            pixmap_item.setPos(j * self.size[0], i * self.size[1])
            self.pixmap_items[i][j][0] = pixmap_item
            self.scene.addItem(pixmap_item)
            if tile.hasEntity():
                pixmap_item = QGraphicsPixmapItem(self.get_pixmap(tile.entity))
                pixmap_item.setPos(j * self.size[0], i * self.size[1])
                self.pixmap_items[i][j][1] = pixmap_item
                self.scene.addItem(pixmap_item)

    def get_pixmap(self, tile):
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
