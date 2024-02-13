from PyQt6.QtCore import *
from utils import Point

from model.grid import Grid
from model.terrains.tile import Tile
from controller.entityInfoController import EntityInfoController

from constants import GRID_HEIGHT, GRID_WIDTH


class GridController:
    """Singleton"""
    instance = None

    def __new__(cls, graphical_grid, simulation, rendering_monitor):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphical_grid = graphical_grid
            cls.simulation = simulation
            cls.rendering_monitor = rendering_monitor
            cls.size = [2048, 2048]
            cls.latest_vertical_value = rendering_monitor.getFirstYVisible()
            cls.latest_horizontal_value = rendering_monitor.getFirstXVisible()
        return cls.instance

    @staticmethod
    def getInstance():
        if GridController.instance is None:
            raise TypeError
        return GridController.instance

    def keyPressEvent(self, event):
        match event.key():
            # player
            case Qt.Key.Key_Z:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((-1, 0)):
                        self.graphical_grid.movePlayer(pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveVerticalScrollBar(-1)
            case Qt.Key.Key_Q:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, -1)):
                        self.graphical_grid.movePlayer(pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveHorizontalScrollBar(-1)
            case Qt.Key.Key_S:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((1, 0)):
                        self.graphical_grid.movePlayer(pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.initSmoothScroll()
            case Qt.Key.Key_D:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, 1)):
                        self.graphical_grid.movePlayer(pos, self.simulation.getPlayer().getPosition())
                        self.graphical_grid.moveHorizontalScrollBar(1)

    def mousePressEvent(self, event):
        scene_pos = self.graphical_grid.mapToScene(event.pos())
        tile = self.getClickedTile(scene_pos.x(), scene_pos.y())
        if tile and tile.hasEntity():
            self.controlEntity(tile)
            #EntityInfoController(tile.getEntity()).draw_entity_info()

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

    def getGridCoordinate(self, x, y):
        i, j = int(y // self.size[1]), int(x // self.size[0])
        if Grid.isInGrid(i, j):
            return i, j
        elif i < 0 or j < 0:
            return 0, 0
        else:
            return GRID_HEIGHT, GRID_WIDTH

    def zoomIn(self):
        if self.rendering_monitor.zoom_index < len(self.rendering_monitor.zooms)-1:
            self.rendering_monitor.zoom_index += 1
            scaler = self.rendering_monitor.zooms[self.rendering_monitor.zoom_index]
            self.rendering_monitor.zoom_factor *= scaler
            self.graphical_grid.scale(scaler, scaler)

            self.recomputeCuboid()

    def recomputeCuboid(self):
        real_rendered_area = self.graphical_grid.mapToScene(self.graphical_grid.viewport().rect()).boundingRect()
        upper, lower, width, height = self.getCuboid(real_rendered_area)
        self.rendering_monitor.setNewPoints(upper, lower, width, height)

    def getCuboid(self, dim: QRectF):
        upper_tile_i, upper_tile_j = self.getGridCoordinate(dim.x(), dim.y())
        lower_tile_i, lower_tile_j = self.getGridCoordinate(dim.x() + dim.width(), dim.y() + dim.height())
        width, height = self.getGridCoordinate(dim.width(), dim.height())
        return [upper_tile_i, upper_tile_j], [lower_tile_i, lower_tile_j], width, height

    def zoomOut(self):
        if self.rendering_monitor.zoom_index > 0:
            scaler = 1/self.rendering_monitor.zooms[self.rendering_monitor.zoom_index]
            self.rendering_monitor.zoom_factor *= scaler
            self.graphical_grid.scale(scaler, scaler)
            self.rendering_monitor.zoom_index -= 1

            self.recomputeCuboid()

    def verticalScroll(self, value):
        ...

    def horizontalScroll(self, value):
        ...