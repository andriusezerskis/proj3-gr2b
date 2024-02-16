from PyQt6.QtCore import *
from utils import Point

from model.grid import Grid
from model.terrains.tile import Tile

from constants import GRID_HEIGHT, GRID_WIDTH

from src.utils import getPointsAdjacentTo


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
            cls.latest_vertical_value = rendering_monitor.getFirstYVisible()
            cls.latest_horizontal_value = rendering_monitor.getFirstXVisible()
        return cls.instance

    @staticmethod
    def getInstance():
        if MainWindowController.instance is None:
            raise TypeError
        return MainWindowController.instance

    def keyPressEvent(self, event):
        match event.key():
            # player
            case Qt.Key.Key_Z:
                self.move_player(Point(0, -1))
            case Qt.Key.Key_Q:
                self.move_player(Point(-1, 0))
            case Qt.Key.Key_S:
                self.move_player(Point(0, 1))
            case Qt.Key.Key_D:
                self.move_player(Point(1, 0))

    def move_player(self, movement):
        if self.simulation.hasPlayer():
            pos = self.simulation.getPlayer().getPos()
            if self.simulation.getPlayer().move(movement):
                self.graphicalGrid.movePlayer(pos, self.simulation.getPlayer().getPos())
                self.graphicalGrid.initSmoothScroll(movement)

    def mousePressEvent(self, event):
        scene_pos = self.graphicalGrid.mapToScene(event.pos())
        tile = self.getClickedTile(scene_pos.x(), scene_pos.y())
        if tile and tile.hasEntity():
            if not self.simulation.hasPlayer():
                if self.graphicalGrid.chosenEntity is not tile.getEntity() and self.graphicalGrid.chosenEntity is not None:
                    self.graphicalGrid.chosenEntity.setHighlighted(False)
                self.mainWindow.entityController.setEntity(tile.getEntity())
                self.mainWindow.entityController.update()
                tile.getEntity().setHighlighted(True)
                self.graphicalGrid.chosenEntity = tile.getEntity()
            else:
                if tile.getPos() in getPointsAdjacentTo(self.simulation.getPlayer().getPos()):
                    tile.removeEntity()
                    self.graphicalGrid.removeEntity(tile.getPos().y(), tile.getPos().x())

    def controlEntity(self, tile):
        if not self.simulation.hasPlayer():
            self.simulation.setPlayerEntity(tile)
            scaler = self.renderingMonitor.zoomForPlayer()
            self.graphicalGrid.scale(scaler, scaler)
            self.recomputeCuboid()
            self.graphicalGrid.removeRenderedSection()
            self.renderingMonitor.centerOnPoint(tile.getIndex())
            self.graphicalGrid.setScrollBars(self.renderingMonitor.getUpperPoint())
            self.graphicalGrid.renderSection()

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
        if self.renderingMonitor.zoom_index < len(self.renderingMonitor.zooms)-1:
            self.renderingMonitor.zoom_index += 1
            scaler = self.renderingMonitor.zooms[self.renderingMonitor.zoom_index]
            self.renderingMonitor.zoom_factor *= scaler
            self.graphicalGrid.scale(scaler, scaler)

            self.recomputeCuboid()

    def recomputeCuboid(self):
        real_rendered_area = self.graphicalGrid.mapToScene(self.graphicalGrid.viewport().rect()).boundingRect()
        upper, lower, width, height = self.getCuboid(real_rendered_area)
        self.renderingMonitor.setNewPoints(upper, lower, width, height)

    def getCuboid(self, dim: QRectF):
        upper_tile_i, upper_tile_j = self.getGridCoordinate(dim.x(), dim.y())
        lower_tile_i, lower_tile_j = self.getGridCoordinate(dim.x() + dim.width(), dim.y() + dim.height())
        width, height = self.getGridCoordinate(dim.width(), dim.height())
        return [upper_tile_i, upper_tile_j], [lower_tile_i, lower_tile_j], width, height

    def zoomOut(self):
        if self.renderingMonitor.zoom_index > 0:
            scaler = 1/self.renderingMonitor.zooms[self.renderingMonitor.zoom_index]
            self.renderingMonitor.zoom_factor *= scaler
            self.graphicalGrid.scale(scaler, scaler)
            self.renderingMonitor.zoom_index -= 1

            self.recomputeCuboid()

    def verticalScroll(self, value):
        ...

    def horizontalScroll(self, value):
        ...

    def closeDockEvent(self):
        self.mainWindow.buttonOpenDock.show()

    def openDockEvent(self):
        print("ahhh")
        self.mainWindow.buttonOpenDock.hide()
        self.mainWindow.dock.show()
