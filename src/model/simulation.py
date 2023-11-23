"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Bloomaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from constants import STEP_TIME
import os
import sys


sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath("constants.py"))))


class Simulation:
    def __init__(self):
        self.grid = None
        self.step = 0

    def run(self):
        print("Starting simulation...")
        end = 0
        start = time.time()
        while True:
            end = time.time()
            if (end-start) > STEP_TIME:
                self.step += 1
                print(self.step)
                # self.grid.step()
                start = time.time()
