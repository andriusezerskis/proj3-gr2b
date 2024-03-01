"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.generator.noiseGenerator import NoiseGenerator
import matplotlib.pyplot as plt
import numpy as np

from parameters import TerrainParameters

from math import sin, pi

from utils import Point


class RegionHandler:

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.gridSize = Point(w, h)
        self.t = 0
        self.flatTemperatureNoise = NoiseGenerator()
        self.flatHumidityNoise = NoiseGenerator()
        self.temperatureMap = np.zeros(
            [self.gridSize.y(), self.gridSize.x()], np.float32)
        self.humidityMap = np.zeros(
            [self.gridSize.y(), self.gridSize.x()], np.float32)
        self._generate()

    def _sampleSineTemperature(self):
        return (TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2 *
                sin(pi * 2 * self.t / TerrainParameters.YEAR_DURATION))

    def _generate(self) -> None:
        self.flatTemperatureNoise.addNoise(3, 1)
        self.flatTemperatureNoise.addNoise(10, 0.3)
        self.flatHumidityNoise.addNoise(3, 1)
        self.flatHumidityNoise.addNoise(10, 0.3)

        for y in range(self.gridSize.y()):
            for x in range(self.gridSize.x()):
                self.temperatureMap[y][x] = self._sampleTemperatureFlat(x, y)
                self.humidityMap[y][x] = self._sampleHumidity(x, y)

    def _sampleTemperatureFlat(self, x: int, y: int):
        s = TerrainParameters.AVERAGE_TEMPERATURE
        s += self.flatTemperatureNoise.sample2D(
            x/self.gridSize.x(), y/self.gridSize.y()) * TerrainParameters.MAX_TEMPERATURE_DIFFERENCE
        return s

    def _sampleHumidity(self, x: int, y: int):
        return self.flatHumidityNoise.sample2D(x/self.gridSize.x(), y/self.gridSize.y())

    def sampleTemperature(self, x: int, y: int) -> float:
        return self.temperatureMap[y][x] + self._sampleSineTemperature()

    def sampleHumidity(self, x: int, y: int) -> float:
        return self.humidityMap[y][x]

    def renderTemperatureMap(self):
        vmin = (TerrainParameters.AVERAGE_TEMPERATURE - TerrainParameters.MAX_TEMPERATURE_DIFFERENCE -
                TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2)
        vmax = (TerrainParameters.AVERAGE_TEMPERATURE + TerrainParameters.MAX_TEMPERATURE_DIFFERENCE +
                TerrainParameters.SEASON_TEMPERATURE_DIFFERENCE / 2)
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
