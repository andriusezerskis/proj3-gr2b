"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.grid import Grid
from model.entities.entity import Entity
from utils import Point, getPointsAdjacentTo, PrioritizedItem
from queue import PriorityQueue


class Pathfinder:

    def __init__(self, grid: Grid):
        self._grid = grid
        self._path: list[Point] | None = None
        self._dists: dict[Point, int] = {}

        # self._moves[point] is the move used to get to "point" from the previous Point in the path
        self._moves: dict[Point, Point] = {}
        self._popped: set[Point] = set()

    @staticmethod
    def _heuristic(current: Point, goal: Point) -> int:
        # octile distance - consistent heuristic
        return max(current.x() - goal.x(), current.y() - goal.y())

    def getPath(self) -> list[Point] | None:
        return self._path

    def _validMovesFromPos(self, entity: Entity, source: Point) -> list[Point]:
        res = []
        for move in getPointsAdjacentTo(Point(0, 0)):
            newPos = source + move
            if self._grid.isPosInGrid(newPos) and type(self._grid.getTile(newPos)) in entity.getValidTiles():
                res.append(move)
        return res

    def _reconstructPath(self, source: Point, destination: Point) -> list[Point]:
        path = []
        currentPos = destination

        # we can simply begin at the destination and go back to the source
        while currentPos != source:
            # move made to go to currentPos
            move = self._moves[currentPos]
            path.append(move)
            currentPos = currentPos - move

        self._path = list(reversed(path))

        return self._path

    def findPath(self, entity: Entity, source: Point, destination: Point) -> bool:
        """
        A*
        :param entity: The entity that needs to pathfind
        :param source: The position of the entity
        :param destination: The position of the destination
        :return: Whether a solution was found
        """
        pqueue = PriorityQueue()
        self._dists[source] = 0

        # PriorizedItem(priority, item)
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

                    # we put the new pos without looking whether it was already in the queue or not, this could be
                    # optimized but there is no direct interface to check the elements of the queue
                    pqueue.put(PrioritizedItem(
                        self._dists[newPos] + self._heuristic(newPos, destination), newPos))

        return False
