"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.simulation import Simulation
from PyQt6.QtWidgets import QApplication, QWidget
import os
import sys


sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("simulation.py"))))


def main():
    print("")


if __name__ == '__main__':
    simulation = Simulation()
    # simulation.run()
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Simulation 2D')
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec())
