from PyQt6.QtCore import *
from utils import Point

from model.grid import Grid
from model.terrains.tile import Tile


class MainWindowController:
    """Singleton"""
    instance = None

    def __new__(cls, graphical_grid, simulation, rendering_monitor, main_window):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphicalGrid = graphical_grid
            cls.mainWindow = main_window
            cls.simulation = simulation
            cls.renderingMonitor = rendering_monitor
            cls.size = [2048, 2048]
        return cls.instance

    @staticmethod
    def getInstance():
        if MainWindowController.instance is None:
            raise TypeError
        return MainWindowController.instance

    def keyPressEvent(self, event):
        match event.key():
            # camera
            case Qt.Key.Key_Up:
                self.graphicalGrid.moveCamera(self.renderingMonitor.up())
            case Qt.Key.Key_Left:
                self.graphicalGrid.moveCamera(self.renderingMonitor.left())
            case Qt.Key.Key_Down:
                self.graphicalGrid.moveCamera(self.renderingMonitor.down())
            case Qt.Key.Key_Right:
                self.graphicalGrid.moveCamera(self.renderingMonitor.right())

            # player
            case Qt.Key.Key_Z:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((-1, 0)):
                        self.graphicalGrid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphicalGrid.moveCamera(
                            self.renderingMonitor.up(False))
            case Qt.Key.Key_Q:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, -1)):
                        self.graphicalGrid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphicalGrid.moveCamera(
                            self.renderingMonitor.left(False))
            case Qt.Key.Key_S:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((1, 0)):
                        self.graphicalGrid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphicalGrid.moveCamera(
                            self.renderingMonitor.down(False))
            case Qt.Key.Key_D:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, 1)):
                        self.graphicalGrid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphicalGrid.moveCamera(
                            self.renderingMonitor.right(False))

    def mousePressEvent(self, event):
        scene_pos = self.graphicalGrid.mapToScene(event.pos())
        tile = self.getClickedTile(scene_pos.x(), scene_pos.y())
        if tile and tile.hasEntity():
            # self.controlEntity(tile)
            if self.graphicalGrid.chosenEntity != tile.getEntity() and self.graphicalGrid.chosenEntity is not None:
                self.graphicalGrid.chosenEntity.setHighlighted(False)
            self.mainWindow.dock2.setEntity(tile.getEntity())
            self.mainWindow.dock2.update()
            tile.getEntity().setHighlighted(True)
            self.graphicalGrid.chosenEntity = tile.getEntity()

    def controlEntity(self, tile):
        if not self.simulation.hasPlayer():
            self.simulation.setPlayerEntity(tile)
            self.graphicalGrid.removeRenderedEntities()
            self.renderingMonitor.centerOnPoint(tile.getIndex())
            self.graphicalGrid.renderEntities()

    def getClickedTile(self, x, y) -> Tile | bool:
        """return false if there is no tile at (x, y) coord"""
        i, j = int(y // self.size[1]), int(x // self.size[0])
        if Grid.isInGrid(i, j):
            return self.simulation.getGrid().getTile(Point(int(x // self.size[0]), int(y // self.size[1])))
        return False

    def wheelEvent(self, event):
        # zoom_out = event.angleDelta().y() < 0
        # zoom_factor = 1.1 if zoom_out else 0.9

        # self.zoom_factor *= zoom_factor
        # self.scale(zoom_factor, zoom_factor)
        return
