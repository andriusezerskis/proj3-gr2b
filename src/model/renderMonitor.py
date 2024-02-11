from typing import List


from model.terrains.tile import Tile
from model.grid import Grid

from constants import RENDERING_HEIGHT, GRID_WIDTH, RENDERING_WIDTH, GRID_HEIGHT



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
        self.rendering_section = Cuboid([(GRID_HEIGHT - RENDERING_HEIGHT) // 2, (GRID_WIDTH - RENDERING_WIDTH) // 2],
                                        [(GRID_HEIGHT + RENDERING_HEIGHT) // 2, (GRID_WIDTH + RENDERING_WIDTH) // 2])

    def left(self, keep_on_screen=True):
        return self.rendering_section.left_move(1, keep_on_screen)

    def right(self, keep_on_screen=True):
        return self.rendering_section.right_move(1, keep_on_screen)

    def up(self, keep_on_screen=True):
        return self.rendering_section.up_move(1, keep_on_screen)

    def down(self, keep_on_screen=True):
        return self.rendering_section.down_move(1, keep_on_screen)

    def getRenderingSection(self):
        return self.rendering_section

    def centerOnPoint(self, point: Tuple[int, int]):
        i, j = point
        self.rendering_section = Cuboid([i - RENDERING_HEIGHT // 2, j - RENDERING_WIDTH // 2],
                                        [i + RENDERING_HEIGHT // 2, j + RENDERING_WIDTH // 2])