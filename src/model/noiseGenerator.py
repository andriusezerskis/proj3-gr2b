from perlin_noise import perlin_noise
from overrides import override


class NoiseGenerator:
    """
    Perlin noise wrapper that supports the summing of different noise with different weights
    """

    def __init__(self):
        self.noises = []
        self.noiseDict = dict()
        self.weightSum = 0

    def addNoise(self, octaves: int, weight: float) -> None:
        """
        Adds a noise component
        :param octaves: The number of octaves (higher means more granular)
        :param weight: The weight in [0; 1]
        """
        self.noises.append((perlin_noise.PerlinNoise(octaves=octaves), weight))
        self.weightSum += weight

    def sample2D(self, x: float, y: float) -> float:
        assert 0 <= x <= 1 and 0 <= y <= 1
        if self.weightSum <= 0:
            raise "The sum of the weights of the noise functions must be > 0"

        if (x, y) in self.noiseDict:
            return self.noiseDict[x, y]
        self.noiseDict[x, y] = sum([noise([x, y]) * weight for noise, weight in self.noises]) / self.weightSum
        return self.noiseDict[x, y]

