"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Bloomaert, Hà Ûyen Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""


from constants import *
import time


class Simulation:
    def __init__(self,  grid):
        self.grid = grid
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
