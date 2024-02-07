import time
from typing import Tuple, List, Set

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMessageBox
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from model.grid import Grid
from model.terrains.tile import Tile
from model.entities.entity import Entity
from model.renderMonitor import RenderMonitor
from model.renderMonitor import Cuboid


class GraphicalGrid(QGraphicsView):

    def __init__(self, grid_size: Tuple[int, int], grid: Grid, simulation):
        self.simulation = simulation
        # super().__init__(*__args)
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.rendering_monitor = RenderMonitor()

        """self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)"""
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
        # self.scale(0.002, 0.002)
        self.scale(0.01, 0.01)

    def updateGrid(self, updated_tiles: Set[Tile]):
        # print(updated_tiles)
        """for tile in updated_tiles:
            self._drawEntities(tile)"""
        for tile in updated_tiles:
            if tile.getIndex() in self.rendering_monitor.get_rendering_section():
                self._drawEntities(tile)

    def drawGrid(self, grid: Grid):
        for tile in grid:
            if tile in self.rendering_monitor.get_rendering_section():
                self._drawTiles(tile)
            else:
                self._drawTerrains(tile)

        """for i, j in self.rendering_monitor.get_rendering_section():
            self._drawTiles(grid.getTile(i, j))"""

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
            # self.pixmap_items[i][j][k].hide()
            # self.pixmap_items[i][j][k].setParentItem(None)
            self.pixmap_items[i][j][k] = None
        if item:
            pixmap_item = QGraphicsPixmapItem(self.getPixmap(item))
            pixmap_item.setPos(j * self.size[0], i * self.size[1])
            self.pixmap_items[i][j][k] = pixmap_item
            self.scene.addItem(pixmap_item)

    def _moveCamera(self, cuboids: Tuple[Cuboid, Cuboid]):
        lost, won = cuboids
        for i, j in lost:
            if self.pixmap_items[i][j][1]:
                self.scene.removeItem(self.pixmap_items[i][j][1])
                self.pixmap_items[i][j][1] = None
        for i, j in won:
            self._drawEntities(self.simulation.getGrid().getTile(i, j))

    def _movePlayer(self, movement):
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

    def keyPressEvent(self, event):
        match event.key():
            # camera
            case Qt.Key.Key_Up:
                self._moveCamera(self.rendering_monitor.up())
            case Qt.Key.Key_Left:
                self._moveCamera(self.rendering_monitor.left())
            case Qt.Key.Key_Down:
                self._moveCamera(self.rendering_monitor.down())
            case Qt.Key.Key_Right:
                self._moveCamera(self.rendering_monitor.right())

            # player
            case Qt.Key.Key_Z:
                if self.simulation.hasPlayer():
                    #self.simulation.getPlayer().move((-1, 0))
                    self._movePlayer((-1, 0))
            case Qt.Key.Key_Q:
                if self.simulation.hasPlayer():
                    #self.simulation.getPlayer().move((0, -1))
                    self._movePlayer((0, -1))
            case Qt.Key.Key_S:
                if self.simulation.hasPlayer():
                    # self.simulation.getPlayer().move((1, 0))
                    self._movePlayer((1, 0))
            case Qt.Key.Key_D:
                if self.simulation.hasPlayer():
                    # self.simulation.getPlayer().move((0, 1))
                    self._movePlayer((0, 1))

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
            self.simulation.setPlayerEntity(tile)
            #self._drawEntityInfo(tile.getEntity())

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
