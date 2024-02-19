"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from enum import Enum


class Action(Enum):
    MOVE = 0
    REPRODUCE = 1
    EAT = 2
    IDLE = 3
