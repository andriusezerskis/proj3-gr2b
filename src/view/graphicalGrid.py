import time
from typing import Tuple, Set, List

from utils import Point

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity
from model.renderMonitor import RenderMonitor
from model.renderMonitor import Cuboid

from controller.gridController import GridController


class GraphicalTile:
    def __init__(self, i: int, j: int):
        self.position = (i, j)
        self.terrain = QLabel()
        self.entity = QLabel()
        self.entity.mousePressEvent = self.mousePressEvent

        self.allows_entity_rendering = False

    def getTerrain(self):
        return self.terrain

    def getEntity(self):
        return self.entity

    def mayRenderEntity(self):
        return self.allows_entity_rendering

    def EnableEntityRendering(self):
        self.allows_entity_rendering = True

    def DisableEntityRendering(self):
        self.allows_entity_rendering = False

    def mousePressEvent(self, event):
        if self.mayRenderEntity():
            GridController.getInstance().mousePressEvent(event, self.position)

    def __iter__(self):
        yield self.terrain
        yield self.entity

    def __getitem__(self, item):
        if item == 0:
            return self.terrain
        elif item == 1:
            return self.entity
        else:
            raise IndexError


class GraphicalGrid(QGridLayout):

    def __init__(self, grid_size: Tuple[int, int], grid: Grid, simulation, parent=None):
        super().__init__(parent)
        self.simulation = simulation
        self.rendering_monitor = RenderMonitor()
        self.gridController = GridController(self, simulation, self.rendering_monitor)
        self.setVerticalSpacing(0)
        self.setHorizontalSpacing(0)
        self.grid_size = grid_size

        self.widgets: List[List[GraphicalTile]] = \
            [[GraphicalTile(j, i) for i in range(self.grid_size[0])] for j in range(self.grid_size[1])]
        self._addWidgets()

        # self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.zoom_step = 0.1

        self.size = 16, 16
        self.pixmap_from_path = {}

        start_time = time.time()
        self.drawGrid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")

    def updateGrid(self, updated_tiles: Set[Tile]):
        for tile in updated_tiles:
            if tile.getIndex() in self.rendering_monitor.getRenderingSection():
                self._drawTiles(tile)

    def drawGrid(self, grid: Grid):
        for tile in grid:
            self._drawTiles(tile)

    def _drawTiles(self, tile):
        self._drawTerrains(tile)
        self._drawEntities(tile)

    def _drawTerrains(self, tile):
        i, j = tile.getIndex()
        self.widgets[i][j].getTerrain().setPixmap(self.getPixmap(tile))

    def _drawEntities(self, tile):
        if tile in self.rendering_monitor.getRenderingSection():
            i, j = tile.getIndex()
            if tile.getEntity():
                self.widgets[i][j].getEntity().setPixmap(self.getPixmap(tile.getEntity()))
            else:
                self.widgets[i][j].getEntity().clear()

    def _removeEntity(self, i, j):
        if self.widgets[i][j][1]:
            self.widgets[i][j][1].clear()

    def _addWidgets(self):
        for i, line in enumerate(self.widgets):
            for j, graphical_tile in enumerate(line):
                if (i, j) in self.rendering_monitor.getRenderingSection() and self.simulation.getGrid().getTile(Point(j, i)).hasEntity():
                    graphical_tile.EnableEntityRendering()
                for label in graphical_tile:
                    self.addWidget(label, i, j)

    def moveCamera(self, cuboids: Tuple[Cuboid, Cuboid]):
        lost, won = cuboids
        for i, j in lost:
            self.widgets[i][j].DisableEntityRendering()
            self.widgets[i][j].getEntity().clear()
        for i, j in won:
            self.widgets[i][j].EnableEntityRendering()
            self._drawTiles(self.simulation.getGrid().getTile(Point(j, i)))

    def getPixmap(self, tile):
        if tile.getTexturePath() not in self.pixmap_from_path:
            pixmap = QPixmap(tile.getTexturePath())
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmap_from_path[tile.getTexturePath()] = pixmap
            return pixmap
        return self.pixmap_from_path[tile.getTexturePath()]

    def movePlayer(self, old_pos, new_pos):
        i, j = old_pos
        self.scene.removeItem(self.widgets[i][j][1])
        self.widgets[i][j][1] = None
        self._drawEntities(
            self.simulation.getGrid().getTile(Point(new_pos[1], new_pos[0])))

    @staticmethod
    def drawEntityInfo(entity: Entity):
        print("bruh")
        entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}\n"
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Entity Information")
        messageBox.setText(entity_info)
        messageBox.setWindowIcon(QIcon(entity.getTexturePath()))
        messageBox.exec()

    # Redirection of PYQT events to the controller
    def wheelEvent(self, event):
        GridController.getInstance().wheelEvent(event)
