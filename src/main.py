"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
import random
import threading
import time

from model.gridGenerator import GridGenerator
from model.simulation import Simulation
from model.gridGenerator import GridGenerator
from PyQt6.QtWidgets import QApplication, QWidget
from model.regionHandler import RegionHandler
import os
import sys

from view.grid import Window
from constants import GRID_WIDTH, GRID_HEIGHT

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("simulation.py"))))


def main():
    print("")


if __name__ == '__main__':
    simulation = Simulation()
    app = QApplication(sys.argv)
    window = Window((GRID_WIDTH, GRID_HEIGHT), simulation)
    simulation.addObserver(window.getGraphicalGrid())
    window.show()
    simulation.run()
    sys.exit(app.exec())
