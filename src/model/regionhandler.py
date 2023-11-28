from model.noiseGenerator import NoiseGenerator
from overrides import override
import matplotlib.pyplot as plt
import numpy as np

from constants import (SEASON_TEMPERATURE_DIFFERENCE, YEAR_DURATION,
                       AVERAGE_TEMPERATURE, MAX_TEMPERATURE_DIFFERENCE, RANDOM_TEMPERATURE_VARIABILITY)
from math import sin, pi


class RegionHandler:

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.t = 0
        self.variableTemperatureNoise = NoiseGenerator()
        self.flatTemperatureNoise = NoiseGenerator()
        self.flatHumidityNoise = NoiseGenerator()
        self.temperatureArrayFlat = np.zeros([self.w, self.h], np.float32)
        self.humidityMap = np.zeros([self.w, self.h], np.float32)
        self._generate()

    def _sampleSineTemperature(self):
        return SEASON_TEMPERATURE_DIFFERENCE / 2 * sin(pi * 2 * self.t / YEAR_DURATION)

    def _generate(self) -> None:
        self.variableTemperatureNoise.addNoise(3, 1)
        self.variableTemperatureNoise.addNoise(10, 0.3)
        self.flatTemperatureNoise.addNoise(3, 1)
        self.flatTemperatureNoise.addNoise(10, 0.3)
        self.flatHumidityNoise.addNoise(3, 1)
        self.flatHumidityNoise.addNoise(10, 0.3)
        self._updateMaps()

    def _sampleTemperature(self, x: int, y: int):
        s = AVERAGE_TEMPERATURE
        # s += self.variableTemperatureNoise.sample3D(x/self.w, y/self.h, self.t/1000) * RANDOM_TEMPERATURE_VARIABILITY
        s += self.flatTemperatureNoise.sample2D(x/self.w, y/self.h) * MAX_TEMPERATURE_DIFFERENCE
        return s

    def _sampleHumidity(self, x: int, y: int):
        return self.flatHumidityNoise.sample2D(x/self.w, y/self.h)

    def _updateMaps(self) -> None:
        for y in range(self.h):
            for x in range(self.w):
                self.temperatureArrayFlat[y][x] = self._sampleTemperature(x, y)
                self.humidityMap[y][x] = self._sampleHumidity(x, y)

    def sampleTemperature(self, x: int, y: int) -> float:
        return self.temperatureArrayFlat[y][x] + self._sampleSineTemperature()

    def sampleHumidity(self, x: int, y: int) -> float:
        return self.humidityMap[y][x]

    def renderTemperatureMap(self):
        vmin = AVERAGE_TEMPERATURE - MAX_TEMPERATURE_DIFFERENCE
        vmax = AVERAGE_TEMPERATURE + MAX_TEMPERATURE_DIFFERENCE
        plt.imshow(self.temperatureArrayFlat + self._sampleSineTemperature(), vmin=vmin, vmax=vmax)
        plt.colorbar()
        plt.draw()
        plt.pause(0.0001)
        plt.clf()

    def advanceTime(self):
        self.t += 1
        # self._updateMaps()
