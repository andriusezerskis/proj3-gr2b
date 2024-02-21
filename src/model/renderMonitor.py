"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from functools import reduce
from typing import List, Tuple

from model.terrains.tile import Tile

from utils import Point


class Cuboid:
    def __init__(self, upperLeftPoint: List, lowerRightPoint: List, size: Point):
        assert isinstance(size, Point)
        self.upper = upperLeftPoint
        self.lower = lowerRightPoint
        self.size = size

    def leftMove(self, dist: int, keepOnScreen: bool):
        saveUpper = self.upper[:]
        saveLower = self.lower[:]
        leftMovement = min(dist, self.upper[1]) if keepOnScreen else dist

        self.upper[1] -= leftMovement
        self.lower[1] -= leftMovement

        lostArea = Cuboid(
            [self.upper[0], self.lower[1] + 1], saveLower, self.size)
        wonArea = Cuboid(
            self.upper, [self.lower[0], saveUpper[1] - 1], self.size)
        return lostArea, wonArea

    def rightMove(self, dist: int, keepOnScreen: bool):
        saveUpper = self.upper[:]
        saveLower = self.lower[:]
        rightMovement = min(dist, self.size[0] - 1 -
                            self.lower[1]) if keepOnScreen else dist

        self.upper[1] += rightMovement
        self.lower[1] += rightMovement

        lostArea = Cuboid(
            saveUpper, [self.lower[0], self.upper[1] - 1], self.size)
        wonArea = Cuboid([self.upper[0], saveLower[1] + 1],
                         self.lower, self.size)
        return lostArea, wonArea

    def upMove(self, dist: int, keepOnScreen: bool):
        saveUpper = self.upper[:]
        saveLower = self.lower[:]
        upMovement = min(dist, self.upper[0]) if keepOnScreen else dist

        self.upper[0] -= upMovement
        self.lower[0] -= upMovement

        lostArea = Cuboid(
            [self.lower[0] + 1, self.upper[1]], saveLower, self.size)
        wonArea = Cuboid(
            self.upper, [saveUpper[0] - 1, self.lower[1]], self.size)
        return lostArea, wonArea

    def downMove(self, dist: int, keepOnScreen: bool):
        saveUpper = self.upper[:]
        saveLower = self.lower[:]
        downMovement = min(dist, self.size[1] - 1 -
                           self.lower[0]) if keepOnScreen else dist

        self.upper[0] += downMovement
        self.lower[0] += downMovement

        lostArea = Cuboid(
            saveUpper, [self.upper[0] - 1, self.lower[1]], self.size)
        wonArea = Cuboid([saveLower[0] + 1, self.upper[1]],
                         self.lower, self.size)
        return lostArea, wonArea

    def __iter__(self):
        for i in range(self.upper[0], self.lower[0] + 1):
            for j in range(self.upper[1], self.lower[1] + 1):
                # if Grid.isInGrid(i, j)
                # if 0 <= i < 100 and 0 <= j < 100:
                yield i, j

    def __contains__(self, item):
        assert isinstance(item, (tuple, list, Tile))
        if isinstance(item, Tile):
            item = item.getPos()
            item = (item.y(), item.x())
        return self.upper[0] <= item[0] <= self.lower[0] and self.upper[1] <= item[1] <= self.lower[1]

    def __repr__(self):
        return f"Cuboid({self.upper}, {self.lower})"


class RenderMonitor:
    def __init__(self, gridSize: Point, size: Point):
        self.renderingSize = size
        self.renderingSection = Cuboid([(gridSize.y() - self.renderingSize.y()) // 2,
                                        (gridSize.x() - self.renderingSize.x()) // 2],
                                       [(gridSize.y() + self.renderingSize.y()) // 2 - 1,
                                        (gridSize.x() + self.renderingSize.x()) // 2 - 1], self.renderingSize)
        self.zoomIndex = 0
        self.zoomFactor = 1
        self.zooms = [1, 4/3, 3/2, 2, 5/2]

    def left(self, dist: int = 1, keepOnScreen: bool = True):
        return self.renderingSection.leftMove(dist, keepOnScreen)

    def right(self, dist: int = 1, keepOnScreen: bool = True):
        return self.renderingSection.rightMove(dist, keepOnScreen)

    def up(self, dist: int = 1, keepOnScreen: bool = True):
        return self.renderingSection.upMove(dist, keepOnScreen)

    def down(self, dist: int = 1, keepOnScreen: bool = True):
        return self.renderingSection.downMove(dist, keepOnScreen)

    def getUpperPoint(self):
        return Point(self.renderingSection.upper[1], self.renderingSection.upper[0])

    def getFirstYVisible(self):
        return self.renderingSection.upper[0]

    def getFirstXVisible(self):
        return self.renderingSection.upper[1]

    def getRenderingSection(self):
        return self.renderingSection

    def setNewPoints(self, upperPoint: List[int], lowerPoint: List[int], width: int, height: int):
        # assert 0 <= lower_point[0] < 100 and 0 <= lower_point[1] < 100
        self.renderingSection = Cuboid(
            upperPoint, lowerPoint, Point(width, height))
        self.renderingSize = Point(width, height)

    def centerOnPoint(self, point: Tuple[int, int]):
        i, j = point
        self.renderingSection = Cuboid([i - self.renderingSize.x() // 2, j - self.renderingSize.y() // 2],
                                       [i + self.renderingSize.x() // 2, j +
                                        self.renderingSize.y() // 2],
                                       self.renderingSize)

    def zoomForPlayer(self):
        oldZoom = self.zoomIndex
        self.zoomIndex = 3
        difference = self.zoomIndex - oldZoom
        if difference > 0:
            newZoom = reduce(lambda x, y: x * y,
                             self.zooms[oldZoom + 1:self.zoomIndex + 1])
            self.zoomFactor *= newZoom
        elif difference < 0:
            newZoom = 1 / \
                reduce(lambda x, y: x * y,
                       self.zooms[oldZoom + 1 + difference:oldZoom+1])
            self.zoomFactor *= newZoom
        else:
            newZoom = 1
        return newZoom
