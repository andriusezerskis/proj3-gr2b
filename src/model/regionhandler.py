from model.noiseGenerator import NoiseGenerator
from overrides import override


class RegionHandler:

    def __init__(self, w: int, h: int):
        self.noiseGenerator = NoiseGenerator(w, h, 20)
        self.w = w
        self.h = h
        self.t = 0

    def _generate(self):
        self.noiseGenerator.addNoise(3, 1)
        self.noiseGenerator.addNoise(10, 0.3)

    def sample(self, x: int, y: int):
        return self.noiseGenerator.sample3D(x, y, self.t)

    def advanceTime(self):
        self.t += 1
