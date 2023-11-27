from perlin_noise import PerlinNoise
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land


class GridGenerator:

    def __init__(self, w: int, h: int, land_threshold: float = 0):
        self.w = w
        self.h = h
        self.land_threshold = land_threshold
        self.noises = []

    def _addNoise(self, octaves: int, weight: float) -> None:
        self.noises.append((PerlinNoise(octaves=octaves), weight))

    def _sample(self, x: int, y: int) -> float:
        return sum([noise([x/self.w, y/self.h]) * weight for noise, weight in self.noises])

    def _generateMatrix(self) -> list[list[Tile]]:
        return [[Water() if self._sample(x, y) < self.land_threshold else Land()
                 for x in range(self.w)] for y in range(self.h)]

    def generateGrid(self) -> list[list[Tile]]:
        self.noises = []
        self._addNoise(4, 1)
        self._addNoise(10, 0.3)
        return self._generateMatrix()
