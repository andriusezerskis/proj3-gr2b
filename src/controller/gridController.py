"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from typing import Tuple

from PyQt6.QtCore import *
from utils import Point


class GridController:
    """Singleton"""
    instance = None

    def __new__(cls, graphicalGrid, simulation, renderingMonitor):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphicalGrid = graphicalGrid
            cls.simulation = simulation
            cls.renderingMonitor = renderingMonitor
            cls.size = [2048, 2048]
            cls.latestVerticalValue = renderingMonitor.getFirstYVisible()
            cls.latestHorizontalValue = renderingMonitor.getFirstXVisible()
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
        if self.simulation.hasPlayer():
            pos = self.simulation.getPlayer().getPos()
            if self.simulation.getPlayer().move(movement):
                self.graphicalGrid.movePlayer(pos, self.simulation.getPlayer().getPos())
                self.graphicalGrid.initSmoothScroll(movement)

    def controlEntity(self, tile):
        if not self.simulation.hasPlayer():
            self.simulation.setPlayerEntity(tile)
            scaler = self.renderingMonitor.setOnZoomIndex()
            self.graphicalGrid.scale(scaler, scaler)
            self.recomputeCuboid()
            self.graphicalGrid.removeRenderedSection()
            self.renderingMonitor.centerOnPoint(tile.getPos())
            self.graphicalGrid.setScrollBars(
                self.renderingMonitor.getUpperPoint())
            self.graphicalGrid.renderSection()

    def getGridCoordinate(self, point: Point, for_cuboid=False) -> Point | None:
        assert isinstance(point, Point)

        board_point = point / Point(self.size[0], self.size[1])
        if self.simulation.getGrid().isInGrid(board_point):
            return board_point

        if for_cuboid:
            if board_point.x() < 0 or board_point.y() < 0:
                return Point(0, 0)
            else:
                return self.simulation.getGrid().getSize() - Point(1, 1)

    def zoomIn(self):
        if self.renderingMonitor.zoomIndex < len(self.renderingMonitor.zooms)-1:
            self.renderingMonitor.zoomIndex += 1
            scaler = self.renderingMonitor.zooms[self.renderingMonitor.zoomIndex]
            self.renderingMonitor.zoomFactor *= scaler
            self.graphicalGrid.scale(scaler, scaler)

            self.recomputeCuboid()

    def recomputeCuboid(self):
        real_rendered_area = self.graphicalGrid.mapToScene(
            self.graphicalGrid.viewport().rect()).boundingRect()
        upper, lower, width, height = self.getCuboid(real_rendered_area)
        self.renderingMonitor.setNewPoints(upper, lower, width, height)

    def getCuboid(self, dim: QRectF) -> Tuple[Point, Point, int, int]:
        upperTile = self.getGridCoordinate(Point(dim.x(), dim.y()), True)
        lowerTile = self.getGridCoordinate(Point(dim.x() + dim.width(), dim.y() + dim.height()), True)
        width, height = self.getGridCoordinate(Point(dim.width(), dim.height()), True)
        return upperTile, lowerTile, width, height

    def zoomOut(self):
        if self.renderingMonitor.zoomIndex > 0:
            scaler = 1 / self.renderingMonitor.zooms[self.renderingMonitor.zoomIndex]
            self.renderingMonitor.zoomFactor *= scaler
            self.graphicalGrid.scale(scaler, scaler)
            self.renderingMonitor.zoomIndex -= 1

            self.recomputeCuboid()
