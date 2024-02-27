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

from model.crafting.crafts import FishingRod, Fence
from model.crafting.loots import Wood, Claw
from model.entities.animals import Crab
from view.startWindow import StartWindow


from PyQt6.QtWidgets import QApplication


signal.signal(signal.SIGINT, signal.SIG_DFL)

sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("simulation.py"))))

LOCALE_LOCK = threading.Lock()

# Locale lock because changing settings of langages is not thread safe
# Timer is a thread so we need a lock


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
    # print(FishingRod.getBlueprint())
    # print(FishingRod.isValidItemType(Wood))
    # print(Fence.getBlueprint())
    # print(Crab._getValidTiles())
    # print(Wood.getDefaultTexturePath())
    # print(Wood.getFrenchName())
    # print(Crab.getLoots())
    # print(Crab.isValidItemType(Claw))
    # print(Crab.getChance(Claw))
    main()
