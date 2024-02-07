from model.grid import Grid
from model.entities.entity import Entity
from utils import Point, euclidDistance, getPointsAdjacentTo, PrioritizedItem
from queue import PriorityQueue


class Pathfinder:

    def __init__(self, grid: Grid):
        self._grid = grid
        self._path: list[Point] | None = None
        self._dists: dict[Point, int] = {}
        self._moves: dict[Point, Point] = {}
        self._popped: set[Point] = set()

    @staticmethod
    def _heuristic(current: Point, goal: Point) -> int:
        # octile distance
        return max(current.x() - goal.x(), current.y() - goal.y())

    def _validMovesFromPos(self, entity: Entity, source: Point) -> list[Point]:
        res = []
        for move in getPointsAdjacentTo(Point(0, 0)):
            newPos = source + move
            if self._grid.isPosInGrid(newPos) and type(self._grid.getTile(newPos)) in entity.getValidTiles():
                res.append(move)
        return res

    def _reconstructPath(self, source: Point, destination: Point) -> list[Point]:
        self._path = []
        currentPos = destination
        while currentPos != source:
            move = self._moves[currentPos]
            self._path.append(move)
            currentPos = currentPos - move
        return self._path

    def findPath(self, entity: Entity, source: Point, destination: Point):
        pqueue = PriorityQueue()
        self._dists[source] = 0

        pqueue.put(PrioritizedItem(0, source))

        while not pqueue.empty():
            item = pqueue.get()
            currentPos = item.item

            if currentPos == destination:
                self._reconstructPath(source, destination)
                return True

            if currentPos in self._popped:
                continue

            self._popped.add(currentPos)

            for move in self._validMovesFromPos(entity, currentPos):
                newPos = currentPos + move

                if (newPos not in self._popped and
                        (newPos not in self._dists.keys() or self._dists[newPos] > self._dists[currentPos] + 1)):

                    self._dists[newPos] = self._dists[currentPos] + 1
                    self._moves[newPos] = move

                    pqueue.put(PrioritizedItem(self._dists[newPos] + self._heuristic(newPos, destination), newPos))

        return False
