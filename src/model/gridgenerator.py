from perlin_noise import PerlinNoise
from model.case import Case


class GridGenerator:

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h

    def generateGrid(self) -> list[list[Case]]:
        noise = PerlinNoise(octaves=4)
        matrix = [["W" if noise([x/self.w, y/self.h]) < 0 else "L" for x in range(self.w)] for y in range(self.h)]
        for l in matrix:
            for c in l:
                print(c, end=" ")
            print()
        return matrix