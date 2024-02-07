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

    def __str__(self):
        return f"({self.x()}, {self.y()})"

    def __repr__(self):
        return str(self)

    def euclidDistance(self, other):
        return abs(self.x() - other.x()) + abs(self.y() - other.y())


def euclidDistance(point1: Point, point2: Point) -> int:
    return point1.euclidDistance(point2)
