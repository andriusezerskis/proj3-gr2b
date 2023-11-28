import noise
from pynoise.noisemodule import Perlin
from pynoise.noiseutil import terrain_gradient, noise_map_plane
from model.noiseGenerator import NoiseGenerator
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land
from model.terrains.sand import Sand


class GridGenerator:

    def __init__(self, w: int, h: int, thresholds=((Water, 0), (Sand, 0.06), (Land, 1))):
        self.noiseGenerator = NoiseGenerator()
        self.w = w
        self.h = h
        #self.noiseGenerator = Perlin()
        #self.noiseMap = noise_map_plane(self.w, self.h, -1, 1, -1, 1, self.noiseGenerator)
        self.thresholds = thresholds

    def _getTile(self, x: int, y: int) -> Tile:
        sample = self.noiseGenerator.sample2D(x/self.w, y/self.h)
        for tileType, threshold in self.thresholds:

            if sample < threshold:
                return tileType((y, x))

    def _generateMatrix(self) -> list[list[Tile]]:
        return [[self._getTile(x, y) for x in range(self.w)] for y in range(self.h)]

    def generateGrid(self) -> list[list[Tile]]:
        self.noiseGenerator.addNoise(4, 1)
        self.noiseGenerator.addNoise(10, 0.3)
        return self._generateMatrix()
