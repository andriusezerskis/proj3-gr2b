import time
from typing import Tuple, List, Set

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity
from model.renderMonitor import RenderMonitor
from model.renderMonitor import Cuboid
from model.simulation import Simulation

from controller.gridController import GridController


class GraphicalGrid(QGraphicsView):

    def __init__(self, grid_size: Tuple[int, int], grid: Grid, simulation: Simulation, rendering_monitor: RenderMonitor):
        self.simulation = simulation
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.rendering_monitor = rendering_monitor

        self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.zoom_step = 0.1

        self.size = 2048, 2048
        self.grid_size = grid_size
        self.pixmap_items: List[List[List[None | QGraphicsPixmapItem]]] = \
            [[[None, None] for _ in range(grid_size[0])]
             for _ in range(grid_size[1])]
        self.pixmap_from_path = {}

        start_time = time.time()
        self.drawGrid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        self.scale(0.01, 0.01)

    def updateGrid(self, updated_tiles: Set[Tile]):
        for tile in updated_tiles:
            if tile.getIndex() in self.rendering_monitor.get_rendering_section():
                self._drawEntities(tile)

    def drawGrid(self, grid: Grid):
        for tile in grid:
            if tile in self.rendering_monitor.get_rendering_section():
                self._drawTiles(tile)
            else:
                self._drawTerrains(tile)

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
            self.pixmap_items[i][j][k] = None
        if item:
            pixmap_item = QGraphicsPixmapItem(self.getPixmap(item))
            pixmap_item.setPos(j * self.size[0], i * self.size[1])
            self.pixmap_items[i][j][k] = pixmap_item
            self.scene.addItem(pixmap_item)

    def moveCamera(self, cuboids: Tuple[Cuboid, Cuboid]):
        lost, won = cuboids
        for i, j in lost:
            if self.pixmap_items[i][j][1]:
                self.scene.removeItem(self.pixmap_items[i][j][1])
                self.pixmap_items[i][j][1] = None
        for i, j in won:
            self._drawEntities(self.simulation.getGrid().getTile(i, j))

    def movePlayer(self, movement):
        i, j = self.simulation.getPlayer().getPosition()
        self.scene.removeItem(self.pixmap_items[i][j][1])
        self.pixmap_items[i][j][1] = None
        self.simulation.getPlayer().move(movement)
        self._drawEntities(self.simulation.getPlayer().getTile())

    def getPixmap(self, tile):
        if tile.getTexturePath() not in self.pixmap_from_path:
            pixmap = QPixmap(tile.getTexturePath())
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmap_from_path[tile.getTexturePath()] = pixmap
            return pixmap
        return self.pixmap_from_path[tile.getTexturePath()]

    def drawEntityInfo(self, entity: Entity):
        entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}\n"
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Entity Information")
        messageBox.setText(entity_info)
        messageBox.setWindowIcon(QIcon(entity.getTexturePath()))
        messageBox.exec()

    # Redirection of PYQT events to the controller
    def keyPressEvent(self, event):
        GridController.getInstance().keyPressEvent(event)

    def mousePressEvent(self, event):
        GridController.getInstance().mousePressEvent(event)

    def wheelEvent(self, event):
        GridController.getInstance().wheelEvent(event)
