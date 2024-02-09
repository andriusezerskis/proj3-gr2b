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

    def __init__(self, grid_size: Tuple[int, int], grid: Grid, simulation, layout):
        self.simulation = simulation
        # super().__init__(*__args)
        self.layout = layout

        self.scene = QGraphicsScene()

        super().__init__(self.scene)
        self.rendering_monitor = RenderMonitor()
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(0)

        self.grid_size = grid_size

        self.layer2widgets = [[None for _ in range(
            self.grid_size[0])]for _ in range(self.grid_size[1])]

        self.layer1widgets = [[None for _ in range(
            self.grid_size[0])]for _ in range(self.grid_size[1])]

        self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.zoom_step = 0.1

        self.size = 16, 16
        self.pixmap_items: List[List[QLabel]] = [
            [[None] for _ in range(grid_size[0])]for _ in range(grid_size[1])]
        self.pixmap_from_path = {}

        start_time = time.time()
        self.drawGrid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")

    def updateGrid(self, updated_tiles: Set[Tile]):
        for tile in updated_tiles:
            if tile.getIndex() in self.rendering_monitor.get_rendering_section():
                if tile.hasEntity():
                    self.layer1widgets[tile.getIndex()[0]][tile.getIndex()[1]].setPixmap(
                        self.getPixmap(tile.getEntity()))

    def drawGrid(self, grid: Grid):

        for tile in grid:
            widget = QLabel()
            widget.setPixmap(self.getPixmap(tile))
            self.layout.addWidget(widget, tile.index[0], tile.index[1])
            self.layer2widgets[tile.getIndex()[0]][tile.getIndex()[1]] = widget

            secondwidget = QLabel()
            self.layer1widgets[tile.getIndex()[0]
                               ][tile.getIndex()[1]] = secondwidget
            if tile.hasEntity():

                secondwidget.setPixmap(self.getPixmap(tile.getEntity()))
                self.layout.addWidget(
                    secondwidget, tile.index[0], tile.index[1])

    def _moveCamera(self, cuboids: Tuple[Cuboid, Cuboid]):
        lost, won = cuboids
        for i, j in lost:
            if self.pixmap_items[i][j][1]:
                self.scene.removeItem(self.pixmap_items[i][j][1])
                self.pixmap_items[i][j][1] = None
        for i, j in won:
            self._drawEntities(self.simulation.getGrid().getTile(i, j))

    def getPixmap(self, tile):
        if tile.getTexturePath() not in self.pixmap_from_path:
            pixmap = QPixmap(tile.getTexturePath())
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmap_from_path[tile.getTexturePath()] = pixmap
            return pixmap
        return self.pixmap_from_path[tile.getTexturePath()]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Z:
            self._moveCamera(self.rendering_monitor.up())
            print("z")
        if event.key() == Qt.Key.Key_Q:
            self._moveCamera(self.rendering_monitor.left())
            print("q")
        if event.key() == Qt.Key.Key_S:
            self._moveCamera(self.rendering_monitor.down())
            print("s")
        if event.key() == Qt.Key.Key_D:
            self._moveCamera(self.rendering_monitor.right())
            print("d")

    def _drawEntityInfo(self, entity: Entity):
        entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}\n"
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Entity Information")
        messageBox.setText(entity_info)
        messageBox.setWindowIcon(QIcon(entity.getTexturePath()))
        messageBox.exec()

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        tile = self.getClickedTile(scene_pos.x(), scene_pos.y())
        if tile.hasEntity():
            self._drawEntityInfo(tile.getEntity())
        # x = scene_pos.x()
        # y = scene_pos.y()
        # print(x, y)
        # print(self.getClickedTile(x, y))

    def getClickedTile(self, x, y):
        """Crash here if not on a pixmap"""
        # print(self.scene.sceneRect().size())
        return self.simulation.getGrid().getTile(int(y // self.size[1]), int(x // self.size[0]))

    """def wheelEvent(self, event):
        # Récupérer le facteur de zoom actuel
        zoom_out = event.angleDelta().y() < 0
        zoom_factor = 1.1 if zoom_out else 0.9

        # Appliquer le zoom
        self.zoom_factor *= zoom_factor
        self.scale(zoom_factor, zoom_factor)"""

    def movePlayer(self, old_pos, new_pos):
        i, j = old_pos
        self.scene.removeItem(self.pixmap_items[i][j][1])
        self.pixmap_items[i][j][1] = None
        self._drawEntities(
            self.simulation.getGrid().getTile(new_pos[0], new_pos[1]))

    @staticmethod
    def drawEntityInfo(entity: Entity):
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
