import time
from typing import Tuple, Set, List
from constants import *

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
from controller.entityInfoController import EntityInfoController

from src.model.simulation import Simulation


class GraphicalTile:
    def __init__(self, i: int, j: int):
        self.position = (i, j)
        self.terrain = QGraphicsPixmapItem()
        self.terrain.setPos(j * 2048, i * 2048)
        self.entity = QGraphicsPixmapItem()
        self.entity.setPos(j * 2048, i * 2048)

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
        self.pixmap_items: List[List[GraphicalTile]] = \
            [[GraphicalTile(i, j) for j in range(self.grid_size[0])]
             for i in range(self.grid_size[1])]
        self._addPixmapItems()
        self.pixmap_from_path = {}

        start_time = time.time()
        self.drawGrid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        self.scale(0.01, 0.01)
        self.initNightMode()

    def initNightMode(self):
        self.luminosityMode = QGraphicsPixmapItem(QPixmap(NIGHT_MODE))
        self.scene.addItem(self.luminosityMode)
        self.luminosityMode.setPos(0, 0)

        pixmap_width = self.luminosityMode.pixmap().width()
        scene_width, scene_height = self.size

        scale = scene_width / pixmap_width if pixmap_width > 0 else 1
        self.luminosityMode.setScale(scale * GRID_HEIGHT)
        self.luminosityMode.show()
        self.luminosityMode.setOpacity(0.7)

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
        self.pixmap_items[i][j].getTerrain().setPixmap(self.getPixmap(tile))

    def _drawEntities(self, tile):
        if tile in self.rendering_monitor.getRenderingSection():
            i, j = tile.getIndex()
            if tile.getEntity():
                self.pixmap_items[i][j].getEntity().setPixmap(
                    self.getPixmap(tile.getEntity()))
            else:
                self.pixmap_items[i][j].getEntity().setPixmap(QPixmap())

    def _removeEntity(self, i, j):
        self.pixmap_items[i][j].getEntity().setPixmap(QPixmap())

    def moveCamera(self, cuboids: Tuple[Cuboid, Cuboid]):
        lost, won = cuboids
        for i, j in lost:
            self.pixmap_items[i][j].DisableEntityRendering()
            self.pixmap_items[i][j].getEntity().setPixmap(QPixmap())
        for i, j in won:
            self.pixmap_items[i][j].EnableEntityRendering()
            self._drawTiles(self.simulation.getGrid().getTile(Point(j, i)))

    def nightMode(self, hour):
        opacity = self.luminosityMode.opacity()
        if hour == SUNSET_MODE_START:
            self.luminosityMode.setPixmap(QPixmap(SUNSET_MODE))
            self.luminosityMode.setOpacity(0.1)
        if hour == NIGHT_MODE_START:
            self.luminosityMode.setPixmap(QPixmap(NIGHT_MODE))
            self.luminosityMode.setOpacity(0.1)

        elif hour == NIGHT_MODE_FINISH:
            self.luminosityMode.setPixmap(QPixmap())
        elif hour > NIGHT_MODE_START or hour < MIDDLE_OF_THE_NIGHT:
            self.luminosityMode.setOpacity(opacity + 0.1)

        elif hour > MIDDLE_OF_THE_NIGHT and hour < NIGHT_MODE_FINISH:
            self.luminosityMode.setOpacity(opacity - 0.1)

    def movePlayer(self, old_pos, new_pos):
        i, j = old_pos
        self.pixmap_items[i][j].getEntity().setPixmap(QPixmap())
        self._drawEntities(self.simulation.getGrid().getTile(
            Point(new_pos[1], new_pos[0])))

    def getPixmap(self, tile):
        if tile.getTexturePath() not in self.pixmap_from_path:
            pixmap = QPixmap(tile.getTexturePath())
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmap_from_path[tile.getTexturePath()] = pixmap
            return pixmap
        return self.pixmap_from_path[tile.getTexturePath()]

    def removeRenderedEntities(self):
        for i, j in self.rendering_monitor.getRenderingSection():
            if self.pixmap_items[i][j][1] is not None:
                self._removeEntity(i, j)

    def renderEntities(self):
        for i, j in self.rendering_monitor.getRenderingSection():
            print(i, j)
            self._drawEntities(self.simulation.getGrid().getTile(Point(j, i)))

    def _addPixmapItems(self):
        for i, line in enumerate(self.pixmap_items):
            for j, graphical_tile in enumerate(line):
                if (i, j) in self.rendering_monitor.getRenderingSection() and self.simulation.getGrid().getTile(Point(j, i)).hasEntity():
                    graphical_tile.EnableEntityRendering()
                for label in graphical_tile:
                    self.scene.addItem(label)

    """@staticmethod
    def drawEntityInfo(entity: Entity):
        entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}"
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Entity Information")
        messageBox.setText(entityInfo)
        messageBox.setWindowIcon(QIcon(entity.getTexturePath()))
        messageBox.exec()"""

    # Redirection of PYQT events to the controller

    def keyPressEvent(self, event):
        GridController.getInstance().keyPressEvent(event)

    def mousePressEvent(self, event):
        GridController.getInstance().mousePressEvent(event)

    def wheelEvent(self, event):
        GridController.getInstance().wheelEvent(event)
