from perlin_noise import PerlinNoise
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land
from model.terrains.sand import Sand


class GridGenerator:

    def __init__(self, w: int, h: int, thresholds=((Water, 0), (Sand, 0.06), (Land, 1))):
        self.w = w
        self.h = h
        self.thresholds = thresholds
        self.noises = []
        self.weight_sum = 0

    def _addNoise(self, octaves: int, weight: float) -> None:
        """
        Adds a noise component
        :param octaves: The number of octaves (higher means more granular)
        :param weight: The weight in [0; 1]
        """
        self.noises.append((PerlinNoise(octaves=octaves), weight))
        self.weight_sum += weight

    def _sample(self, x: int, y: int) -> float:
        return sum([noise([x/self.w, y/self.h]) * weight for noise, weight in self.noises])

    def _getTile(self, x: int, y: int) -> Tile:
        sample = self._sample(x, y)
        for tileType, threshold in self.thresholds:
            # self._sample() returns a value in [-self.weight_sum; self.weight_sum]
            # because without weight, noise() returns a value in [-1; 1]
            if sample < threshold * self.weight_sum:
                return tileType((y, x))

    def _generateMatrix(self) -> list[list[Tile]]:
        return [[self._getTile(x, y) for x in range(self.w)] for y in range(self.h)]

    def generateGrid(self) -> list[list[Tile]]:
        self.noises = []
        self._addNoise(4, 1)
        self._addNoise(10, 0.3)
        return self._generateMatrix()
