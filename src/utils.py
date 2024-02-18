from dataclasses import dataclass, field
from typing import Any


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
