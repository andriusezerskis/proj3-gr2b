from perlin_noise import perlin_noise
from overrides import override


class NoiseGenerator:
    """
    Perlin noise wrapper that supports the summing of different noise with different weights
    """

    def __init__(self):
        self.noises = []
        self.weight_sum = 0

    def addNoise(self, octaves: int, weight: float) -> None:
        """
        Adds a noise component
        :param octaves: The number of octaves (higher means more granular)
        :param weight: The weight in [0; 1]
        """
        self.noises.append((perlin_noise.PerlinNoise(octaves=octaves), weight))
        self.weight_sum += weight

    def sample2D(self, x: float, y: float) -> float:
        assert 0 <= x <= 1 and 0 <= y <= 1
        if self.weight_sum <= 0:
            raise "The sum of the weights of the noise functions must be > 0"

        return sum([noise([x, y]) * weight for noise, weight in self.noises]) / self.weight_sum

    def sample3D(self, x: float, y: float, z: float) -> float:
        assert 0 <= x <= 1 and 0 <= y <= 1 and 0 <= z <= 1
        if self.weight_sum <= 0:
            raise "The sum of the weights of the noise functions must be > 0"

        return sum([noise([x, y, z]) * weight for noise, weight in self.noises]) / self.weight_sum
