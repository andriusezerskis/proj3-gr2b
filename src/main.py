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
import os
import sys

from view.grid import Window

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("simulation.py"))))


def main():
    print("")


if __name__ == '__main__':
    objet = GridGenerator(10, 10)
    objet.generateGrid()
    simulation = Simulation()
    # simulation.run()
    app = QApplication(sys.argv)
    window = Window((200, 200), [[random.choice(["LH", "LC", "LP", "L", "W", "W", "W", "W", "L", "L", "L"])
                                  for _ in range(200)] for _ in range(200)])
    window.show()
    sys.exit(app.exec())
