"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from dataclasses import dataclass, field
from typing import Any
from math import atan2, sqrt, acos


class Point:
    """
    Wrapper for a 2D point
    """

    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

    def x(self):
        return self._x

    def y(self) -> int:
        return self._y

    def __add__(self, other):
        return Point(self.x() + other.x(), self.y() + other.y())

    def __sub__(self, other):
        return Point(self.x() - other.x(), self.y() - other.y())

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x() * other, self.y() * other)
        elif isinstance(other, Point):
            return Point(self.x() * other.x(), self.y() * other.y())

    def __truediv__(self, other):
        if isinstance(other, int):
            return Point(self.x() // other, self.y() // other)
        elif isinstance(other, Point):
            return Point(self.x() // other.x(), self.y() // other.y())

    def __str__(self):
        return f"({self.x()}, {self.y()})"

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return Point(self.x(), self.y())

    def __neg__(self):
        return Point(-self.x(), -self.y())

    def __hash__(self):
        return hash((self.x(), self.y()))

    def __eq__(self, other):
        return self.x() == other.x() and self.y() == other.y()

    def euclidDistance(self, other):
        return abs(self.x() - other.x()) + abs(self.y() - other.y())

    def isNextTo(self, other) -> bool:
        return self.octileDistance(other) == 1

    def octileDistance(self, other):
        return max(abs(self.x() - other.x()), abs(self.y() - other.y()))

    def __iter__(self):
        yield self.x()
        yield self.y()


class Point3D:
    """
    Wrapper for a 3D point
    """

    def __init__(self, x: float, y: float, z: float):
        self._x: float = x
        self._y: float = y
        self._z: float = z

    def x(self) -> float:
        return self._x

    def y(self) -> float:
        return self._y

    def z(self) -> float:
        return self._z

    def __add__(self, other):
        return Point3D(self.x() + other.x(), self.y() + other.y(), self.z() + other.z())

    def __sub__(self, other):
        return Point3D(self.x() - other.x(), self.y() - other.y(), self.z() - other.z())

    def __truediv__(self, other: float):
        assert isinstance(other, float)
        return Point3D(self.x() / other, self.y() / other, self.z() / other)

    def __str__(self):
        return f"({self.x()}, {self.y()}, {self.z()})"

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return Point3D(self.x(), self.y(), self.z())

    def __neg__(self):
        return Point3D(-self.x(), -self.y(), -self.z())

    def __hash__(self):
        return hash((self.x(), self.y(), self.z()))

    def round(self):
        return Point3D(round(self.x()), round(self.y()), round(self.z()))

    def dotProd(self, other) -> float:
        return self.x() * other.x() + self.y() * other.y() + self.z() * other.z()

    def crossProd(self, other):
        return Point3D(self.y() * other.z() - self.z() * other.y(),
                       self.z() * other.x() - self.x() * other.z(),
                       self.x() * other.y() - self.y() * other.x())

    def norm(self) -> float:
        return sqrt(self.x() ** 2 + self.y() ** 2 + self.z() ** 2)

    def normalized(self):
        return self / self.norm()

    def angle(self, other) -> float:
        return acos(self.dotProd(other) / sqrt((self.x() ** 2 + self.y() ** 2 + self.z() ** 2) *
                                               (other.x() ** 2 + other.y() ** 2 + other.z() ** 2)))

    # def angle(self, other) -> float:
    #     # https://stackoverflow.com/a/33920320
    #     return atan2(self.crossProd(other).dotProd(self.crossProd(other).normalized()), self.dotProd(other))


# https://docs.python.org/3/library/queue.html
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def euclidDistance(point1: Point, point2: Point) -> int:
    return point1.euclidDistance(point2)


def getPointsAdjacentTo(point: Point) -> list[Point]:
    return getPointsInRadius(point, 1)


def getPointsInRadius(point: Point, radius: int) -> list[Point]:
    assert radius > 0 and isinstance(radius, int)
    return [Point(point.x() + x, point.y() + y) for y in range(-radius, radius + 1) for x in range(-radius, radius + 1)
            if x != 0 or y != 0]
