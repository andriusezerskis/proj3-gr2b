"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.generator.noiseGenerator import NoiseGenerator
import matplotlib.pyplot as plt
import numpy as np

from constants import (SEASON_TEMPERATURE_DIFFERENCE, YEAR_DURATION,
                       AVERAGE_TEMPERATURE, MAX_TEMPERATURE_DIFFERENCE)
from math import sin, pi


class RegionHandler:

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.t = 0
        self.flatTemperatureNoise = NoiseGenerator()
        self.flatHumidityNoise = NoiseGenerator()
        self.temperatureMap = np.zeros([self.w, self.h], np.float32)
        self.humidityMap = np.zeros([self.w, self.h], np.float32)
        self._generate()

    def _sampleSineTemperature(self):
        return SEASON_TEMPERATURE_DIFFERENCE / 2 * sin(pi * 2 * self.t / YEAR_DURATION)

    def _generate(self) -> None:
        self.flatTemperatureNoise.addNoise(3, 1)
        self.flatTemperatureNoise.addNoise(10, 0.3)
        self.flatHumidityNoise.addNoise(3, 1)
        self.flatHumidityNoise.addNoise(10, 0.3)

        for y in range(self.h):
            for x in range(self.w):
                self.temperatureMap[y][x] = self._sampleTemperatureFlat(x, y)
                self.humidityMap[y][x] = self._sampleHumidity(x, y)

    def _sampleTemperatureFlat(self, x: int, y: int):
        s = AVERAGE_TEMPERATURE
        s += self.flatTemperatureNoise.sample2D(
            x/self.w, y/self.h) * MAX_TEMPERATURE_DIFFERENCE
        return s

    def _sampleHumidity(self, x: int, y: int):
        return self.flatHumidityNoise.sample2D(x/self.w, y/self.h)

    def sampleTemperature(self, x: int, y: int) -> float:
        return self.temperatureMap[y][x] + self._sampleSineTemperature()

    def sampleHumidity(self, x: int, y: int) -> float:
        return self.humidityMap[y][x]

    def renderTemperatureMap(self):
        vmin = (AVERAGE_TEMPERATURE - MAX_TEMPERATURE_DIFFERENCE -
                SEASON_TEMPERATURE_DIFFERENCE / 2)
        vmax = (AVERAGE_TEMPERATURE + MAX_TEMPERATURE_DIFFERENCE +
                SEASON_TEMPERATURE_DIFFERENCE / 2)
        plt.imshow(self.temperatureMap + self._sampleSineTemperature(),
                   vmin=vmin, vmax=vmax)
        plt.text(1, 4, f"t={self.t}", backgroundcolor="white")
        plt.colorbar()
        plt.draw()
        # plt.savefig(f"../assets/steps/{self.t}.png")
        plt.pause(0.0001)
        plt.clf()

    def advanceTime(self):
        self.t += 1
