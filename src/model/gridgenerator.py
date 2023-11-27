from perlin_noise import PerlinNoise
from model.noiseGenerator import NoiseGenerator
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land
from model.terrains.sand import Sand


class GridGenerator:

    def __init__(self, w: int, h: int, thresholds=((Water, 0), (Sand, 0.06), (Land, 1))):
        self.noiseGenerator = NoiseGenerator(w, h)
        self.w = w
        self.h = h
        self.thresholds = thresholds

    def _getTile(self, x: int, y: int) -> Tile:
        sample = self.noiseGenerator.sample2D(x, y)
        for tileType, threshold in self.thresholds:
            # self._sample() returns a value in [-self.weight_sum; self.weight_sum]
            # because without weight, noise() returns a value in [-1; 1]
            if sample < threshold * self.noiseGenerator.weight_sum:
                return tileType((y, x))

    def _generateMatrix(self) -> list[list[Tile]]:
        return [[self._getTile(x, y) for x in range(self.w)] for y in range(self.h)]

    def generateGrid(self) -> list[list[Tile]]:
        self.noiseGenerator.addNoise(4, 1)
        self.noiseGenerator.addNoise(10, 0.3)
        return self._generateMatrix()
