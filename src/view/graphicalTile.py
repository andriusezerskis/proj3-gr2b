"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from constants import FIRE, ICE, TEXTURE_SIZE, Disaster


class GraphicalTile:
    def __init__(self, i: int, j: int):
        self.position = (i, j)
        self.terrain = QGraphicsPixmapItem()
        self.terrain.setPos(j * TEXTURE_SIZE, i * TEXTURE_SIZE)
        self.entity = QGraphicsPixmapItem()
        self.entity.setPos(j * TEXTURE_SIZE, i * TEXTURE_SIZE)
        self.filter = QGraphicsPixmapItem()
        self.filter.setPos(j * TEXTURE_SIZE, i * TEXTURE_SIZE)
        self.disasterFilter = QGraphicsPixmapItem()
        self.disasterFilter.setPos(j * TEXTURE_SIZE, i * TEXTURE_SIZE)

    def getTerrain(self):
        return self.terrain

    def getEntity(self):
        return self.entity

    def getFilter(self):
        return self.filter

    def getDisasterFilter(self):
        return self.disasterFilter

    def __iter__(self):
        yield self.terrain
        yield self.filter
        yield self.entity
        yield self.disasterFilter

    def __getitem__(self, item):
        if item == 0:
            return self.terrain
        elif item == 1:
            return self.entity
        else:
            raise IndexError
