from functools import reduce
from typing import List, Tuple

from model.terrains.tile import Tile
from model.grid import Grid

from constants import RENDERING_HEIGHT, GRID_WIDTH, RENDERING_WIDTH, GRID_HEIGHT

from utils import Point


class Cuboid:
    def __init__(self, upper_left_point: List, lower_right_point: List):
        self.upper = upper_left_point
        self.lower = lower_right_point

    def left_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        left_movement = min(dist, self.upper[1]) if keep_on_screen else dist

        self.upper[1] -= left_movement
        self.lower[1] -= left_movement

        lost_area = Cuboid([self.upper[0], self.lower[1] + 1], save_lower)
        won_area = Cuboid(self.upper, [self.lower[0], save_upper[1] - 1])
        return lost_area, won_area

    def right_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        right_movement = min(dist, GRID_WIDTH - 1 - self.lower[1]) if keep_on_screen else dist

        self.upper[1] += right_movement
        self.lower[1] += right_movement

        lost_area = Cuboid(save_upper, [self.lower[0], self.upper[1] - 1])
        won_area = Cuboid([self.upper[0], save_lower[1] + 1], self.lower)
        return lost_area, won_area

    def up_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        up_movement = min(dist, self.upper[0]) if keep_on_screen else dist

        self.upper[0] -= up_movement
        self.lower[0] -= up_movement

        lost_area = Cuboid([self.lower[0] + 1, self.upper[1]], save_lower)
        won_area = Cuboid(self.upper, [save_upper[0] - 1, self.lower[1]])
        return lost_area, won_area

    def down_move(self, dist: int, keep_on_screen: bool):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        down_movement = min(dist, GRID_HEIGHT - 1 - self.lower[0]) if keep_on_screen else dist

        self.upper[0] += down_movement
        self.lower[0] += down_movement

        lost_area = Cuboid(save_upper, [self.upper[0] - 1, self.lower[1]])
        won_area = Cuboid([save_lower[0] + 1, self.upper[1]], self.lower)
        return lost_area, won_area

    def __iter__(self):
        for i in range(self.upper[0], self.lower[0] + 1):
            for j in range(self.upper[1], self.lower[1] + 1):
                if Grid.isInGrid(i, j):
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
    def __init__(self):
        self.rendering_size = Point(GRID_WIDTH, GRID_HEIGHT)
        self.rendering_section = Cuboid([(GRID_HEIGHT - self.rendering_size.y()) // 2,
                                         (GRID_WIDTH - self.rendering_size.x()) // 2],
                                        [(GRID_HEIGHT + self.rendering_size.y()) // 2,
                                         (GRID_WIDTH + self.rendering_size.x()) // 2])
        self.zoom_index = 0
        self.zoom_factor = 1
        self.zooms = [1, 4/3, 3/2, 2, 5/2]

    def left(self, dist: int = 1, keep_on_screen: bool = True):
        return self.rendering_section.left_move(dist, keep_on_screen)

    def right(self, dist: int = 1, keep_on_screen: bool = True):
        return self.rendering_section.right_move(dist, keep_on_screen)

    def up(self, dist: int = 1, keep_on_screen: bool = True):
        return self.rendering_section.up_move(dist, keep_on_screen)

    def down(self, dist: int = 1, keep_on_screen: bool = True):
        return self.rendering_section.down_move(dist, keep_on_screen)

    def getUpperPoint(self):
        return Point(self.rendering_section.upper[1], self.rendering_section.upper[0])

    def getFirstYVisible(self):
        return self.rendering_section.upper[0]

    def getFirstXVisible(self):
        return self.rendering_section.upper[1]

    def getRenderingSection(self):
        return self.rendering_section

    def setNewPoints(self, upper_point: List[int], lower_point: List[int], width: int, height: int):
        self.rendering_section = Cuboid(upper_point, lower_point)
        self.rendering_size = Point(width, height)

    def centerOnPoint(self, point: Tuple[int, int]):
        i, j = point
        self.rendering_section = Cuboid([i - self.rendering_size.x() // 2, j - self.rendering_size.y() // 2],
                                        [i + self.rendering_size.x() // 2, j + self.rendering_size.y() // 2])

    def zoomForPlayer(self):
        old_zoom = self.zoom_index
        self.zoom_index = 3
        difference = self.zoom_index - old_zoom
        if difference > 0:
            new_zoom = reduce(lambda x, y: x * y, self.zooms[old_zoom + 1:self.zoom_index + 1])
            self.zoom_factor *= new_zoom
        elif difference < 0:
            new_zoom = 1 / reduce(lambda x, y: x * y, self.zooms[old_zoom + 1 + difference:old_zoom+1])
            self.zoom_factor *= new_zoom
        else:
            new_zoom = 1
        return new_zoom
