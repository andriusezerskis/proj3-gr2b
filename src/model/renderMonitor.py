"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from functools import reduce
from typing import TypeVar, List

from model.terrains.tile import Tile
from utils import Point

Cuboid_ = TypeVar("Cuboid_")


class Cuboid:
    """Represents a rectangle that covers the area between
    the given upper left point, and the lower right point (both included)"""

    def __init__(self, upperLeftPoint: Point, lowerRightPoint: Point, component: List[Cuboid_] = None):
        assert isinstance(upperLeftPoint, Point)
        assert isinstance(lowerRightPoint, Point)
        self.upper = upperLeftPoint
        self.lower = lowerRightPoint
        self.component: List[Cuboid_] = component

    def __iter__(self):
        for y in range(self.upper.y(), self.lower.y() + 1):
            for x in range(self.upper.x(), self.lower.x() + 1):
                if not self.component or (Point(x, y) in self.component[1] and not Point(x, y) in self.component[0]):
                    yield Point(x, y)

    def __contains__(self, item):
        assert isinstance(item, (Point, Tile))
        if isinstance(item, Tile):
            item = item.getPos()
        return self.upper.x() <= item.x() <= self.lower.x() and self.upper.y() <= item.y() <= self.lower.y()

    def getArea(self):
        return self.getWidth() * self.getHeight()

    def getHeight(self):
        return self.lower.y() - self.upper.y() + 1

    def getWidth(self):
        return self.lower.x() - self.upper.x() + 1

    def __repr__(self):
        return f"Cuboid({self.upper}, {self.lower})"

    def __eq__(self, other):
        return self.upper == other.upper and self.lower == other.lower

    def isEqual(self, upper, lower):
        return self.upper == upper and self.lower == lower

    def setConstraint(self, constraint):
        self.component = constraint

    def difference(self, other: Cuboid_):
        return Cuboid(Point(min(self.upper.x(), other.upper.x()), min(self.upper.y(), other.upper.y())),
                      Point(max(self.lower.x(), other.lower.x()), max(self.lower.y(), other.lower.y())),
                      [self, other])


class RenderMonitor:
    """Represents the visible section of the grid for the user"""

    def __init__(self, gridSize: Point, size: Point):
        assert isinstance(gridSize, Point)
        assert isinstance(size, Point)
        self.gridSize = gridSize
        self.renderingSize = size
        self.renderingSection = Cuboid(Point(0, 0), Point(
            gridSize.x() - 1, gridSize.y() - 1))

        self.zoomIndex = 0
        self.zoomFactor = 1
        self.zooms = [1, 4 / 3, 3 / 2, 2, 5 / 2, 2]
        self.playerZoomFactor = None

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
        new_section = Cuboid(upperPoint, lowerPoint)
        difference = self.renderingSection.difference(new_section)
        self.renderingSection = new_section
        self.renderingSize = Point(width, height)
        return difference

    def centerOnPoint(self, point: Point):
        assert isinstance(point, Point)
        upper = point - self.renderingSize // 2
        upper = Point(0 if not upper.xIsPositive() else upper.x(),
                      0 if not upper.yIsPositive() else upper.y())
        lower = point + self.renderingSize // 2
        lower = self.gridSize - \
                Point(1, 1) if not lower < self.gridSize else lower

        self.renderingSection = Cuboid(upper, lower)

    def setOnZoomIndex(self, index=3):
        oldZoom = self.getZoomIndex()
        self.zoomIndex = index
        difference = self.getZoomIndex() - oldZoom
        if difference > 0:
            newZoom = reduce(lambda x, y: x * y,
                             self.zooms[oldZoom + 1:self.getZoomIndex() + 1])
            self.multiplyZoomFactor(newZoom)
        elif difference < 0:
            newZoom = 1 / reduce(lambda x, y: x * y,
                                 self.zooms[oldZoom + 1 + difference:oldZoom + 1])
            self.multiplyZoomFactor(newZoom)
        else:
            newZoom = 1
        return newZoom

    def getAreaScalerFactor(self, area=100):
        self.playerZoomFactor = round(1 / ((area / (self.renderingSection.getArea())) ** (1 / 2)), 3)
        return self.playerZoomFactor

    def isNextToBorder(self, point: Point, movement: Point):
        upper_borders = point - self.renderingSize // 2
        lower_borders = point + self.renderingSize // 2 - self.gridSize
        if (movement.x() and (not upper_borders.xIsPositive() or lower_borders.xIsPositive())) \
                or (movement.y() and (not upper_borders.yIsPositive() or lower_borders.yIsPositive())):
            return True
        return False

    def isMaximumZoomIndex(self):
        return self.getZoomIndex() == len(self.zooms) - 1

    def isMinimumZoomIndex(self):
        return self.getZoomIndex() == 0

    def getZoomFactor(self):
        return self.playerZoomFactor if self.playerZoomFactor is not None else self.zoomFactor

    def getZoomIndex(self):
        return self.zoomIndex

    def resetPlayerZoomFactor(self):
        zoom = self.getZoomFactor()
        self.playerZoomFactor = None
        return 1 / zoom

    def multiplyZoomFactor(self, coeff):
        self.zoomFactor *= coeff
