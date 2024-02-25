"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtCore import *
from utils import Point

from model.terrains.tile import Tile

from src.utils import getPointsAdjacentTo


class MainWindowController:
    """Singleton"""
    instance = None

    def __new__(cls, graphicalGrid, simulation, mainWindow):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphicalGrid = graphicalGrid
            cls.mainWindow = mainWindow
            cls.simulation = simulation
            cls.size = [2048, 2048]
        return cls.instance

    @staticmethod
    def getInstance():
        if MainWindowController.instance is None:
            raise TypeError
        return MainWindowController.instance

    def getClickedTile(self, x, y) -> Tile | bool:
        """return false if there is no tile at (x, y) coord"""
        i, j = int(y // self.size[1]), int(x // self.size[0])
        if 0 <= i < self.size[1] and 0 <= j < self.size[0]:
            return self.simulation.getGrid().getTile(Point(int(x // self.size[0]), int(y // self.size[1])))
        return False

    def mousePressEvent(self, event):
        """Handles the mouse press event

        Args:
            event (_type_): the mouse press event
        """
        scenePos = self.graphicalGrid.mapToScene(event.pos())
        tile = self.getClickedTile(scenePos.x(), scenePos.y())
        if tile:
            if self.mainWindow.monitor.getIsMonitor():
                self.mainWindow.monitor.offIsMonitor()
                zone, radius, disaster = self.mainWindow.monitor.getInfo()
                self.simulation.bordinatorExecution(
                    zone,  radius, disaster, tile.getPos())

            elif tile.hasEntity():
                if not self.simulation.hasPlayer():
                    self.openDockEvent()
                else:
                    if tile.getPos() in getPointsAdjacentTo(self.simulation.getPlayer().getPos()):
                        tile.removeEntity()
                        self.graphicalGrid.removeEntity(
                            tile.getPos().y(), tile.getPos().x())

            self.mainWindow.entityController.setEntity(
                tile.getEntity())
            self.graphicalGrid.chosenEntity = tile.getEntity()
            self.mainWindow.entityController.update()
            self.graphicalGrid.updateHighlighted()

    def closeDockEvent(self):
        self.mainWindow.buttonOpenDock.show()

    def openDockEvent(self):
        self.mainWindow.buttonOpenDock.hide()
        self.mainWindow.dock.show()
