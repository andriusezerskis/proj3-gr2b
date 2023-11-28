"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
import random
from model.gridgenerator import GridGenerator
from model.simulation import Simulation
from model.gridgenerator import GridGenerator
from PyQt6.QtWidgets import QApplication, QWidget
from model.regionhandler import RegionHandler
import os
import sys

from view.grid import Window

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("simulation.py"))))


def main():
    print("")


def test_region():
    import matplotlib.pyplot as plt
    import numpy as np
    regions = RegionHandler(100, 100)
    while True:
        regions.renderTemperatureMap()
        regions.advanceTime()
        if regions.t >= 100:
            break



if __name__ == '__main__':
    objet = GridGenerator(100, 100)
    test_region()
    # objet.generateGrid()
    # simulation = Simulation()
    # simulation.run()
    app = QApplication(sys.argv)
    window = Window((200, 200), objet.generateGrid())
    window.show()
    sys.exit(app.exec())
