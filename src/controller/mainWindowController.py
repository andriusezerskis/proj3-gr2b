from PyQt6.QtCore import *
from utils import Point

from model.grid import Grid
from model.terrains.tile import Tile
from controller.entityInfoController import EntityInfoController


class MainWindowController:
    """Singleton"""
    instance = None

    def __new__(cls, graphical_grid, simulation, rendering_monitor, main_window):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphical_grid = graphical_grid
            cls.main_window = main_window
            cls.simulation = simulation
            cls.rendering_monitor = rendering_monitor
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
                self.graphical_grid.moveCamera(self.rendering_monitor.up())
            case Qt.Key.Key_Left:
                self.graphical_grid.moveCamera(self.rendering_monitor.left())
            case Qt.Key.Key_Down:
                self.graphical_grid.moveCamera(self.rendering_monitor.down())
            case Qt.Key.Key_Right:
                self.graphical_grid.moveCamera(self.rendering_monitor.right())

            # player
            case Qt.Key.Key_Z:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((-1, 0)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveCamera(
                            self.rendering_monitor.up(False))
            case Qt.Key.Key_Q:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, -1)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveCamera(
                            self.rendering_monitor.left(False))
            case Qt.Key.Key_S:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((1, 0)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveCamera(
                            self.rendering_monitor.down(False))
            case Qt.Key.Key_D:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, 1)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveCamera(
                            self.rendering_monitor.right(False))

    def mousePressEvent(self, event):
        scene_pos = self.graphical_grid.mapToScene(event.pos())
        tile = self.getClickedTile(scene_pos.x(), scene_pos.y())
        if tile and tile.hasEntity():
            # self.controlEntity(tile)
            print("here")
            self.main_window.dock2.updateOnClick(tile.getEntity())
            # à faire, fonctionne pas encore
            EntityInfoController(tile.getEntity()).draw_entity_info()

    def controlEntity(self, tile):
        if not self.simulation.hasPlayer():
            self.simulation.setPlayerEntity(tile)
            self.graphical_grid.removeRenderedEntities()
            self.rendering_monitor.centerOnPoint(tile.getIndex())
            self.graphical_grid.renderEntities()

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