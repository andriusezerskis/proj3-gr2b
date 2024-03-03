"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

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
            return Point(int(self.x() // other), int(self.y() // other))
        elif isinstance(other, Point):
            return Point(int(self.x() // other.x()), int(self.y() // other.y()))

    def __floordiv__(self, other):
        return self.__truediv__(other)

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
    
    def manhattanDistance(self, other):
        return abs(self.x() - other.x()) + abs(self.y() - other.y())

    def isPositive(self):
        return self.x() >= 0 and self.y() >= 0

    def __lt__(self, other):
        return self.x() < other.x() and self.y() < other.y()

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


def getTerminalSubclassesOfClass(cls: type) -> set[type]:
    res = set()
    stack = [cls]
    while len(stack) > 0:
        current = stack.pop()
        subclasses = current.__subclasses__()
        if len(subclasses) == 0:
            res.add(current)
        else:
            stack.extend(subclasses)
    return res

def getFrenchToEnglishTranslation(frenchEntity: str) -> str:
    return {
        "Crabe": "Crab",
        "Poisson": "Fish",
        "Arbre": "Tree",
        "Plante": "Plant",
        "Algue": "Algae",
        "Humain": "Human"
    }[frenchEntity]