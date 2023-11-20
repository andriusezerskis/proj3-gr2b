"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget


def main():
    print("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Simulation 2D')
    window.setGeometry(100, 100, 400, 300)
    window.show()
    sys.exit(app.exec())
