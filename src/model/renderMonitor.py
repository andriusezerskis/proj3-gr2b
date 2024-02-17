from functools import reduce
from typing import List, Tuple

from model.terrains.tile import Tile
from model.grid import Grid

from constants import RENDERING_HEIGHT, RENDERING_WIDTH

from utils import Point


class Cuboid:
    def __init__(self, upper_left_point: List, lower_right_point: List, size: Point):
        assert isinstance(size, Point)
        self.upper = upper_left_point
        self.lower = lower_right_point
        self.size = size

    def left_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        left_movement = min(dist, self.upper[1]) if keep_on_screen else dist

        self.upper[1] -= left_movement
        self.lower[1] -= left_movement

        lost_area = Cuboid(
            [self.upper[0], self.lower[1] + 1], save_lower, self.size)
        won_area = Cuboid(
            self.upper, [self.lower[0], save_upper[1] - 1], self.size)
        return lost_area, won_area

    def right_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        right_movement = min(dist, self.size - 1 -
                             self.lower[1]) if keep_on_screen else dist

        self.upper[1] += right_movement
        self.lower[1] += right_movement

        lost_area = Cuboid(
            save_upper, [self.lower[0], self.upper[1] - 1], self.size)
        won_area = Cuboid([self.upper[0], save_lower[1] + 1],
                          self.lower, self.size)
        return lost_area, won_area

    def up_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        up_movement = min(dist, self.upper[0]) if keep_on_screen else dist

        self.upper[0] -= up_movement
        self.lower[0] -= up_movement

        lost_area = Cuboid(
            [self.lower[0] + 1, self.upper[1]], save_lower, self.size)
        won_area = Cuboid(
            self.upper, [save_upper[0] - 1, self.lower[1]], self.size)
        return lost_area, won_area

    def down_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        down_movement = min(dist, self.size - 1 -
                            self.lower[0]) if keep_on_screen else dist

        self.upper[0] += down_movement
        self.lower[0] += down_movement

        lost_area = Cuboid(
            save_upper, [self.upper[0] - 1, self.lower[1]], self.size)
        won_area = Cuboid([save_lower[0] + 1, self.upper[1]],
                          self.lower, self.size)
        return lost_area, won_area

    def __iter__(self):
        print(self.upper, self.lower)
        for i in range(self.upper[0], self.lower[0] + 1):
            for j in range(self.upper[1], self.lower[1] + 1):
                #if Grid.isInGrid(i, j)
                #if 0 <= i < 100 and 0 <= j < 100:
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
    def __init__(self, grid_size: Point, size: Point):
        self.renderingSize = size
        self.renderingSection = Cuboid([(grid_size.y() - self.renderingSize.y()) // 2,
                                        (grid_size.x() - self.renderingSize.x()) // 2],
                                       [(grid_size.y() + self.renderingSize.y()) // 2 - 1,
                                        (grid_size.x() + self.renderingSize.x()) // 2 - 1], self.renderingSize)
        self.zoomIndex = 0
        self.zoomFactor = 1
        self.zooms = [1, 4/3, 3/2, 2, 5/2]

    def left(self, dist: int = 1, keep_on_screen: bool = True):
        return self.renderingSection.left_move(dist, keep_on_screen)

    def right(self, dist: int = 1, keep_on_screen: bool = True):
        return self.renderingSection.right_move(dist, keep_on_screen)

    def up(self, dist: int = 1, keep_on_screen: bool = True):
        return self.renderingSection.up_move(dist, keep_on_screen)

    def down(self, dist: int = 1, keep_on_screen: bool = True):
        return self.renderingSection.down_move(dist, keep_on_screen)

    def getUpperPoint(self):
        return Point(self.renderingSection.upper[1], self.renderingSection.upper[0])

    def getFirstYVisible(self):
        return self.renderingSection.upper[0]

    def getFirstXVisible(self):
        return self.renderingSection.upper[1]

    def getRenderingSection(self):
        return self.renderingSection

    def setNewPoints(self, upper_point: List[int], lower_point: List[int], width: int, height: int):
        #assert 0 <= lower_point[0] < 100 and 0 <= lower_point[1] < 100
        self.renderingSection = Cuboid(upper_point, lower_point, Point(width, height))
        self.renderingSize = Point(width, height)

    def centerOnPoint(self, point: Tuple[int, int]):
        i, j = point
        self.renderingSection = Cuboid([i - self.renderingSize.x() // 2, j - self.renderingSize.y() // 2],
                                       [i + self.renderingSize.x() // 2, j + self.renderingSize.y() // 2],
                                       self.renderingSize)

    def zoomForPlayer(self):
        old_zoom = self.zoomIndex
        self.zoomIndex = 3
        difference = self.zoomIndex - old_zoom
        if difference > 0:
            new_zoom = reduce(lambda x, y: x * y,
                              self.zooms[old_zoom + 1:self.zoomIndex + 1])
            self.zoomFactor *= new_zoom
        elif difference < 0:
            new_zoom = 1 / \
                reduce(lambda x, y: x * y,
                       self.zooms[old_zoom + 1 + difference:old_zoom+1])
            self.zoomFactor *= new_zoom
        else:
            new_zoom = 1
        return new_zoom
