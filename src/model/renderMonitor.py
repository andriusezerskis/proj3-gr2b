from typing import List, Tuple

from constants import *

from model.terrains.tile import Tile


class Cuboid:
    def __init__(self, upper_left_point: List, lower_right_point: List):
        self.upper = upper_left_point
        self.lower = lower_right_point

    def left_move(self, left_dist):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        left_movement = min(left_dist, self.upper[1])

        self.upper[1] -= left_movement
        self.lower[1] -= left_movement

        lost_area = Cuboid([self.upper[0], self.lower[1] + 1], save_lower)
        won_area = Cuboid(self.upper, [self.lower[0], save_upper[1] - 1])
        return lost_area, won_area

    def right_move(self, right_dist):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        right_movement = min(right_dist, GRID_WIDTH - 1 - self.lower[1])

        self.upper[1] += right_movement
        self.lower[1] += right_movement

        lost_area = Cuboid(save_upper, [self.lower[0], self.upper[1] - 1])
        won_area = Cuboid([self.upper[0], save_lower[1] + 1], self.lower)
        return lost_area, won_area

    def up_move(self, up_dist):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        up_movement = min(up_dist, self.upper[0])

        self.upper[0] -= up_movement
        self.lower[0] -= up_movement

        lost_area = Cuboid([self.lower[0] + 1, self.upper[1]], save_lower)
        won_area = Cuboid(self.upper, [save_upper[0] - 1, self.lower[1]])
        return lost_area, won_area

    def down_move(self, down_dist):
        save_upper = self.upper[:]
        save_lower = self.lower[:]
        down_movement = min(down_dist, GRID_HEIGHT - 1 - self.lower[0])
        print(down_movement)

        self.upper[0] += down_movement
        self.lower[0] += down_movement

        lost_area = Cuboid(save_upper, [self.upper[0] - 1, self.lower[1]])
        won_area = Cuboid([save_lower[0] + 1, self.upper[1]], self.lower)
        return lost_area, won_area

    def left_line_gt(self, value):
        return self.upper[1] > value

    def right_line_lt(self, value):
        return self.upper[1] < value

    def up_line_gt(self, value):
        return self.upper[0] > value

    def down_line_lt(self, value):
        return self.upper[0] < value

    def getLine(self, i) -> List[Tuple[int, int]]:
        return [(i, j) for j in range(self.upper[0], 1, self.lower[0])]

    def getColumn(self, j) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(self.upper[1], 1, self.lower[1])]

    def __iter__(self):
        for i in range(self.upper[0], self.lower[0] + 1):
            for j in range(self.upper[1], self.lower[1] + 1):
                yield i, j

    def __contains__(self, item):
        assert isinstance(item, (tuple, list, Tile))
        if isinstance(item, Tile):
            item = item.getIndex()
        return self.upper[0] <= item[0] <= self.lower[0] and self.upper[1] <= item[1] <= self.lower[1]

    def __repr__(self):
        return f"Cuboid({self.upper}, {self.lower})"


class RenderMonitor:
    def __init__(self):
        self.rendering_section = Cuboid([(GRID_HEIGHT - RENDERING_HEIGHT) // 2, (GRID_WIDTH - RENDERING_WIDTH) // 2],
                                        [(GRID_HEIGHT + RENDERING_HEIGHT) // 2, (GRID_WIDTH + RENDERING_WIDTH) // 2])

    def left(self):
        return self.rendering_section.left_move(1)

    def right(self):
        return self.rendering_section.right_move(1)

    def up(self):
        return self.rendering_section.up_move(1)

    def down(self):
        return self.rendering_section.down_move(1)

    def get_rendering_section(self):
        return self.rendering_section