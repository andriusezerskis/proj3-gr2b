"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from utils import Point, getPointsAdjacentTo

from model.terrains.tile import Tile

from constants import TEXTURE_SIZE
from controller.gridController import GridController


class MainWindowController:
    """Singleton"""
    instance = None

    def __new__(cls, graphicalGrid, simulation, mainWindow):
        if cls.instance is None:
            print("eueueeuueeuueeueueueueueueueueeuueuu")
            cls.instance = object.__new__(cls)
            cls.graphicalGrid = graphicalGrid
            cls.mainWindow = mainWindow
            cls.simulation = simulation
            # cls.gridController = GridController.getInstance()
        return cls.instance

    @staticmethod
    def getInstance():
        if MainWindowController.instance is None:
            raise TypeError
        return MainWindowController.instance

    def getClickedTile(self, point: Point) -> Tile | bool:
        """return false if there is no tile at (x, y) coord"""
        board_point = point // self.graphicalGrid.texture_size
        if self.simulation.getGrid().isInGrid(board_point):
            return self.simulation.getGrid().getTile(board_point)
        return False

    def mousePressEvent(self, event):
        """Handles the mouse press event

        Args:
            event (_type_): the mouse press event
        """
        scenePos = self.graphicalGrid.mapToScene(event.pos())
        tile = self.getClickedTile(Point(scenePos.x(), scenePos.y()))
        if tile:
            if self.mainWindow.docksMonitor.getCurrentDock().monitor.getIsMonitor():
                self.mainWindow.docksMonitor.getCurrentDock().monitor.offIsMonitor()
                zone, radius, disaster = self.mainWindow.docksMonitor.getCurrentDock().monitor.getInfo()
                tiles = self.simulation.bordinatorExecution(zone, radius, disaster, tile.getPos())
                self.graphicalGrid.updateGrid(tiles)

            elif tile.hasEntity():
                if not self.simulation.hasPlayer():
                    self.openDockEvent()
                else:
                    self.playerControll(tile)
                    return

            self.mainWindow.docksMonitor.getCurrentDock().entityController.setEntity(tile.getEntity())
            self.graphicalGrid.chosenEntity = tile.getEntity()
            self.mainWindow.docksMonitor.getCurrentDock().entityController.update()
            self.graphicalGrid.updateHighlighted()

    def playerControll(self, tile):
        if tile.getPos() in getPointsAdjacentTo(self.simulation.getPlayer().getPos()):
            tile.getEntity()
            tile.removeEntity()
            self.graphicalGrid.removeEntity(tile.getPos())

            self.graphicalGrid.updateHighlighted()

    def closeDock(self):
        self.mainWindow.docksMonitor.getCurrentDock().close()

    def closeDockEvent(self):
        self.mainWindow.buttonOpenDock.show()

    def changeDock(self):
        self.mainWindow.docksMonitor.changeCurrentDock()

    def hide_button(self):
        self.mainWindow.buttonOpenDock.hide()

    def openDockEvent(self):
        self.mainWindow.buttonOpenDock.hide()
        self.mainWindow.docksMonitor.openDock()
