"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from utils import Point, getPointsAdjacentTo

from model.terrains.tile import Tile

from model.crafting.crafts import FishingRod

from parameters import ViewParameters

from model.terrains.tiles import Water


class MainWindowController:
    """Singleton"""
    instance = None

    def __new__(cls, graphicalGrid, simulation, mainWindow):
        if cls.instance is None:
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
        board_point = point // self.graphicalGrid.textureSize
        if self.simulation.getGrid().isInGrid(board_point):
            return self.simulation.getGrid().getTile(board_point)
        return False

    def mousePressEvent(self, event):
        """Handles the mouse press event

        Args:
            event (Event): the mouse press event
        """
        if not self.graphicalGrid.isDefaultTileRenderer():
            return
        scenePos = self.graphicalGrid.mapToScene(event.pos())
        tile = self.getClickedTile(Point(scenePos.x(), scenePos.y()))

        fish_click = False
        if self.simulation.hasPlayer() and self.simulation.getPlayer().isFishing():
            fish_click = True
            self.raiseHook()

        if tile:
            if self.mainWindow.docksMonitor.isMonitoringDock() and \
                    self.mainWindow.docksMonitor.getCurrentDock().monitor.getIsMonitor():
                self.mainWindow.docksMonitor.getCurrentDock().monitor.offIsMonitor()
                zone, radius, disaster, entityChosen = self.mainWindow.docksMonitor.getCurrentDock().monitor.getInfo()
                tiles = self.simulation.bordinatorExecution(zone, radius, disaster, entityChosen, tile.getPos())
                self.graphicalGrid.updateGrid(tiles)

            if not self.simulation.hasPlayer():
                if not self.mainWindow.docksMonitor.isDisplayed():
                    self.openDockEvent()
                self.mainWindow.docksMonitor.getCurrentDock().entityController.setEntity(tile.getEntity())
                self.graphicalGrid.chosenEntity = tile.getEntity()
                self.mainWindow.docksMonitor.getCurrentDock().entityController.update()
                self.graphicalGrid.updateHighlighted()
            elif not fish_click:
                self.playerControll(tile)
                return

            if not tile.hasEntity() and not self.simulation.hasPlayer():
                self.graphicalGrid.chosenEntity = None
                self.graphicalGrid.updateHighlighted()
                self.mainWindow.docksMonitor.getCurrentDock().entityController.view.deselectEntity()

    def mouseReleaseEvent(self, event):
        """End of hook throwing"""
        if self.simulation.hasPlayer() and isinstance(self.simulation.getPlayer().getTargetedTileForHooking(), Water):
            fallingPlace = self.simulation.getPlayer().throwHook()
            if isinstance(self.simulation.getGrid().getTile(fallingPlace), Water):
                self.graphicalGrid.drawHook(fallingPlace)
            else:
                print("pêche échouée")
                self.graphicalGrid.stopHooking()
                self.simulation.getPlayer().stopFishing()

    def raiseHook(self):
        tile = self.simulation.getGrid().getTile(self.simulation.getPlayer().getHookPlace())
        if tile.hasEntity():
            print("vous avez pêché " + str(self.simulation.getPlayer().getHookPlace()))
            entity = tile.getEntity()
            self.simulation.player.addInInventory(entity.loot())
            self.mainWindow.docksMonitor.getCurrentDock().scrollArea.update_content(
                self.simulation.player.getInventory())
            tile.removeEntity()
            entity.kill()
            self.graphicalGrid.redraw(tile)
        else:
            print("NAK " + str(self.simulation.getPlayer().getHookPlace()))
        self.simulation.getPlayer().stopFishing()
        self.graphicalGrid.removeHook()

    def EntityMonitorPressEvent(self, event):
        ...

    def playerControll(self, tile):
        if tile.hasEntity() and tile.getPos() in getPointsAdjacentTo(self.simulation.getPlayer().getPos()):
            entity = tile.getEntity()
            self.simulation.player.addInInventory(entity.loot())
            self.mainWindow.docksMonitor.getCurrentDock().scrollArea.update_content(
                self.simulation.player.getInventory())
            tile.removeEntity()
            entity.kill()
            self.graphicalGrid.redraw(tile)

            self.graphicalGrid.updateHighlighted()
        elif isinstance(tile, Water) and self.simulation.getPlayer().canFish():
            print("start")
            self.simulation.getPlayer().startFishing(tile)
            self.graphicalGrid.startHooking()

    def unlockFishing(self):
        if not self.simulation.getPlayer().abilityUnlockedRod and self.simulation.getPlayer().hasEnoughQuantityToCraft(FishingRod):
            self.simulation.getPlayer().abilityUnlockedRod = True
            self.simulation.getPlayer().removeFromInventory(FishingRod.getBlueprint())
            self.mainWindow.docksMonitor.getCurrentDock().scrollArea.update_content(
                self.simulation.player.getInventory())
            return True
        return False

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

    def onEntityControl(self):
        self.mainWindow.zoomInButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        self.mainWindow.zoomOutButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        self.mainWindow.changeTileRendererButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        self.mainWindow.docksMonitor.getCurrentDock().scrollArea.update_content(
            self.simulation.player.getInventory())

    def onEntityLage(self):
        self.mainWindow.zoomInButton.setStyleSheet(None)
        self.mainWindow.zoomOutButton.setStyleSheet(None)
        self.mainWindow.changeTileRendererButton.setStyleSheet(None)

    def onZoomIn(self):
        if self.simulation.renderMonitor.isMaximumZoomIndex():
            self.mainWindow.zoomInButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        else:
            self.mainWindow.zoomOutButton.setStyleSheet(None)

    def onZoomOut(self):
        if self.simulation.renderMonitor.isMinimumZoomIndex():
            self.mainWindow.zoomOutButton.setStyleSheet(ViewParameters.LOCKED_BUTTON)
        else:
            self.mainWindow.zoomInButton.setStyleSheet(None)