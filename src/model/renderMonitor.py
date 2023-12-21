from constants import *


class Cuboid:
    def __init__(self, upper_left_point, lower_right_point):
        self.upper = upper_left_point
        self.lower = lower_right_point

    def move(self, up_dist, left_dist):
        new_up = self.upper[0] - up_dist
        new_left = self.upper[1] - left_dist
        if new_up < 0:
            up_dist += new_up

        if new_left < 0:
            left_dist += new_left

            self.upper[0] -= up_dist
            self.lower[0] -= up_dist
            self.upper[1] -= left_dist
            self.upper[1] -= left_dist

    def left_line_gt(self, value):
        return self.upper[1] > value

    def right_line_lt(self, value):
        return self.upper[1] < value

    def up_line_gt(self, value):
        return self.upper[0] > value

    def down_line_lt(self, value):
        return self.upper[0] < value

    def __iter__(self):
        for i in range(self.upper[0], self.lower[0] + 1):
            for j in range(self.upper[1], self.lower[1] + 1):
                yield i, j

    def __contains__(self, item):
        assert isinstance(item, tuple)
        return self.upper[0] <= item[0] <= self.lower[0] and self.upper[1] <= item[1] <= self.lower[1]


class RenderMonitor:
    def __init__(self):
        self.rendering_section = Cuboid(((GRID_HEIGHT - RENDERING_HEIGHT) // 2, (GRID_WIDTH - RENDERING_WIDTH) // 2),
                                        ((GRID_HEIGHT + RENDERING_HEIGHT) // 2, (GRID_WIDTH + RENDERING_WIDTH) // 2))

    def left(self):
        self.rendering_section.move(0, 1)

    def right(self):
        self.rendering_section.move(0, -1)

    def up(self):
        self.rendering_section.move(1, 0)

    def down(self):
        self.rendering_section.move(-1, 0)

    def get_rendering_section(self):
        return self.rendering_section
