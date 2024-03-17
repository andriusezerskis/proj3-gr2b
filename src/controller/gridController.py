"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from typing import Tuple

from PyQt6.QtCore import *
from utils import Point

from controller.mainWindowController import MainWindowController


class GridController:
    """Singleton"""
    instance = None

    def __new__(cls, graphicalGrid, simulation, renderingMonitor):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphicalGrid = graphicalGrid
            cls.simulation = simulation
            cls.renderingMonitor = renderingMonitor
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
                self.movePlayer(Point(0, -1))
            case Qt.Key.Key_Q:
                self.movePlayer(Point(-1, 0))
            case Qt.Key.Key_S:
                self.movePlayer(Point(0, 1))
            case Qt.Key.Key_D:
                self.movePlayer(Point(1, 0))

    def movePlayer(self, movement):
        if self.simulation.hasPlayer() and not self.simulation.player.isFishing():
            pos = self.simulation.getPlayer().getPos()
            if self.simulation.getPlayer().move(movement):
                self.graphicalGrid.movePlayer(pos, self.simulation.getPlayer().getPos())
                if not self.renderingMonitor.isNextToBorder(self.simulation.getPlayer().getPos() if movement.isPositive() else pos, movement):
                    self.graphicalGrid.initSmoothScroll(movement)

    def controlEntity(self, tile):
        if not self.simulation.hasPlayer():
            self.simulation.setPlayerEntity(tile)
            scaler = self.renderingMonitor.setOnZoomIndex()
            #self.graphicalGrid.scale(1, 1)
            #scaler = self.renderingMonitor.getAreaScalerFactor()
            #print(scaler)
            self.graphicalGrid.scale(scaler, scaler)
            self.recomputeCuboid()
            self.graphicalGrid.removeRenderedSection()
            self.renderingMonitor.centerOnPoint(tile.getPos())
            self.graphicalGrid.setScrollBars(self.renderingMonitor.getUpperPoint())
            self.graphicalGrid.renderSection()

    def lageEntity(self):
        if self.simulation.getPlayer().isFishing():
            self.graphicalGrid.removeHook()
        player_pos = self.simulation.getPlayer().getPos()
        self.simulation.getPlayer().removeClaimedEntity()
        self.graphicalGrid.chosenEntity = self.simulation.getGrid().getTile(player_pos).getEntity()

    def resizeEvent(self, event):
        if not self.simulation.hasPlayer():
            if self.renderingMonitor.getRenderingSize() != self.simulation.getGrid().getSize():
                self.recomputeCuboid()
        else:
            if self.renderingMonitor.getRenderingSize() != self.simulation.getGrid().getSize():
                self.recomputeCuboid()
            """if self.renderingMonitor.getRenderingSize() != self.simulation.getGrid().getSize():
                scaler = self.renderingMonitor.getAreaScalerFactor()
                self.graphicalGrid.scale(scaler, scaler)
                self.recomputeCuboid()"""

    def getGridCoordinate(self, point: Point, for_cuboid=False, is_size=False) -> Point | None:
        """return the coordinate in the grid of a point on the screen
        if for_cuboid is True, points outside the board returns the min/max point"""
        assert isinstance(point, Point)

        board_point = point / self.graphicalGrid.textureSize
        if self.simulation.getGrid().isInGrid(board_point):
            return board_point

        if for_cuboid:
            if board_point.x() < 0 or board_point.y() < 0:
                return Point(0, 0)
            else:
                size = self.simulation.getGrid().getSize()
                return size if is_size else size - Point(1, 1)

    def zoomIn(self):
        if self.simulation.hasPlayer():
            return

        if self.renderingMonitor.getZoomIndex() < len(self.renderingMonitor.zooms)-1:
            self.renderingMonitor.zoomIndex += 1
            scaler = self.renderingMonitor.zooms[self.renderingMonitor.getZoomIndex()]
            self.renderingMonitor.multiplyZoomFactor(scaler)
            self.graphicalGrid.scale(scaler, scaler)

            MainWindowController.getInstance().onZoomIn()
            self.recomputeCuboid()

    def recomputeCuboid(self):
        real_rendered_area = self.graphicalGrid.mapToScene(self.graphicalGrid.viewport().rect()).boundingRect()
        upper, lower, width, height = self.getCuboid(real_rendered_area)
        if not self.renderingMonitor.getRenderingSection().isEqual(upper, lower):
            self.graphicalGrid.redrawSection(self.renderingMonitor.setNewPoints(upper, lower, width, height))

    def getCuboid(self, dim: QRectF) -> Tuple[Point, Point, int, int]:
        upperTile = self.getGridCoordinate(Point(dim.x(), dim.y()), True)
        lowerTile = self.getGridCoordinate(

            Point(dim.x() + dim.width(), dim.y() + dim.height()), True)
        width, height = self.getGridCoordinate(

            Point(dim.width(), dim.height()), True, True)
        return upperTile, lowerTile, width, height

    def zoomOut(self):
        if self.simulation.hasPlayer():
            return

        if self.renderingMonitor.getZoomIndex() > 0:
            scaler = 1 / self.renderingMonitor.zooms[self.renderingMonitor.getZoomIndex()]
            self.renderingMonitor.multiplyZoomFactor(scaler)
            self.graphicalGrid.scale(scaler, scaler)
            self.renderingMonitor.zoomIndex -= 1

            MainWindowController.getInstance().onZoomOut()
            self.recomputeCuboid()
