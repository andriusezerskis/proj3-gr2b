"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from functools import reduce

from model.terrains.tile import Tile
from utils import Point


class Cuboid:
    """Represents a rectangle that covers the area between
    the given upper left point, and the lower right point (both included)"""

    def __init__(self, upperLeftPoint: Point, lowerRightPoint: Point, size: Point):
        assert isinstance(size, Point)
        assert isinstance(upperLeftPoint, Point)
        assert isinstance(lowerRightPoint, Point)
        self.upper = upperLeftPoint
        self.lower = lowerRightPoint
        self.size = size

    def __iter__(self):
        # print(f"y: {self.upper.y()} to {self.lower.y() + 1} ; x: {self.upper.x()} to {self.lower.x() + 1}")
        for y in range(self.upper.y(), self.lower.y() + 1):
            for x in range(self.upper.x(), self.lower.x() + 1):
                yield Point(x, y)

    def __contains__(self, item):
        assert isinstance(item, (Point, Tile))
        if isinstance(item, Tile):
            item = item.getPos()
        return self.upper.x() <= item.x() <= self.lower.x() and self.upper.y() <= item.y() <= self.lower.y()

    def __repr__(self):
        return f"Cuboid({self.upper}, {self.lower})"


class RenderMonitor:
    """Represents the visible section of the grid for the user"""

    def __init__(self, gridSize: Point, size: Point):
        assert isinstance(gridSize, Point)
        assert isinstance(size, Point)
        self.gridSize = gridSize
        self.renderingSize = size
        self.renderingSection = Cuboid(Point(0, 0), Point(gridSize.x() - 1, gridSize.y() - 1), self.renderingSize)

        self.zoomIndex = 0
        self.zoomFactor = 1
        self.zooms = [1, 4 / 3, 3 / 2, 2, 5 / 2, 2]

    def getUpperPoint(self):
        return self.renderingSection.upper

    def getFirstYVisible(self):
        return self.renderingSection.upper.y()

    def getFirstXVisible(self):
        return self.renderingSection.upper.x()

    def getRenderingSection(self):
        return self.renderingSection

    def getRenderingSize(self):
        return self.renderingSize

    def setNewPoints(self, upperPoint: Point, lowerPoint: Point, width: int, height: int):
        assert isinstance(upperPoint, Point)
        assert isinstance(lowerPoint, Point)
        self.renderingSection = Cuboid(upperPoint, lowerPoint, Point(width, height))
        self.renderingSize = Point(width, height)

    def centerOnPoint(self, point: Point):
        assert isinstance(point, Point)
        upper = point - self.renderingSize // 2
        upper = Point(0 if not upper.xIsPositive() else upper.x(), 0 if not upper.yIsPositive() else upper.y())
        lower = point + self.renderingSize // 2
        lower = self.gridSize - Point(1, 1) if not lower < self.gridSize else lower

        self.renderingSection = Cuboid(upper, lower, self.renderingSize)

    def setOnZoomIndex(self, index=3):
        oldZoom = self.zoomIndex
        self.zoomIndex = index
        difference = self.zoomIndex - oldZoom
        if difference > 0:
            newZoom = reduce(lambda x, y: x * y, self.zooms[oldZoom + 1:self.zoomIndex + 1])
            self.zoomFactor *= newZoom
        elif difference < 0:
            newZoom = 1 / reduce(lambda x, y: x * y, self.zooms[oldZoom + 1 + difference:oldZoom + 1])
            self.zoomFactor *= newZoom
        else:
            newZoom = 1
        return newZoom

    def isNextToBorder(self, point: Point, movement: Point):
        upper_borders = point - self.renderingSize // 2
        lower_borders = point + self.renderingSize // 2 - self.gridSize
        if (movement.x() and (not upper_borders.xIsPositive() or lower_borders.xIsPositive())) \
                or (movement.y() and (not upper_borders.yIsPositive() or lower_borders.yIsPositive())):
            return True
        return False

    def isMaximumZoomIndex(self):
        return self.zoomIndex == len(self.zooms) - 1

    def isMinimumZoomIndex(self):
        return self.zoomIndex == 0
