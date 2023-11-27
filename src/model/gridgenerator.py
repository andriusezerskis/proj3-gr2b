from perlin_noise import PerlinNoise
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land


class GridGenerator:

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h

    def generateGrid(self) -> list[list[Tile]]:
        noise = PerlinNoise(octaves=4)
        matrix = [[Water((y, x)) if noise([x/self.w, y/self.h]) < 0 else Land((y, x))
                   for x in range(self.w)] for y in range(self.h)]
        for l in matrix:
            for c in l:
                print(c.getType(), end=" ")
            print()
        return matrix
