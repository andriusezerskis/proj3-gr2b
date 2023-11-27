from perlin_noise import PerlinNoise
from overrides import override


class NoiseGenerator:
    """
    Perlin noise wrapper that supports the summing of different noise with different weights
    """

    def __init__(self, w: int, h: int, z: int = 1_000_000):
        self.w = w
        self.h = h
        self.z = z
        self.noises = []
        self.weight_sum = 0

    def addNoise(self, octaves: int, weight: float) -> None:
        """
        Adds a noise component
        :param octaves: The number of octaves (higher means more granular)
        :param weight: The weight in [0; 1]
        """
        self.noises.append((PerlinNoise(octaves=octaves), weight))
        self.weight_sum += weight

    def sample2D(self, x: int, y: int) -> float:
        assert 0 <= x < self.w and 0 <= y

        return sum([noise([x/self.w, y/self.h]) * weight for noise, weight in self.noises])

    def sample3D(self, x: int, y: int, z: int) -> float:
        assert 0 <= x < self.w and 0 <= y < self.h and 0 <= z < self.z

        return sum([noise([x/self.w, y/self.h, z/self.z]) * weight
                    for noise, weight in self.noises])
