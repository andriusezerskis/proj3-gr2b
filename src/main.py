"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from contextlib import contextmanager
import locale
import threading
import os
import sys
import signal
from view.startWindow import StartWindow


from PyQt6.QtWidgets import QApplication

# from constants import GRID_WIDTH, GRID_HEIGHT

from model.simulation import Simulation

from view.mainWindow import Window


signal.signal(signal.SIGINT, signal.SIG_DFL)

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("simulation.py"))))

LOCALE_LOCK = threading.Lock()

# Locale lock because changing settings of langages is not thread safe
# Timer is a thread so we need a lock rip


@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


def main():
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    app = QApplication(sys.argv)
    startWindow = StartWindow()
    startWindow.show()
    app.exec()


if __name__ == '__main__':
    main()
