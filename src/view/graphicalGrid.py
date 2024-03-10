"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from enum import Enum
from typing import Set, List, Type

from PyQt6.QtCore import QTimer, Qt, QLineF
from controller.gridController import GridController

from utils import Point

from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from model.grid import Grid
from model.terrains.tile import Tile
from model.renderMonitor import RenderMonitor

from controller.mainWindowController import MainWindowController

from view.tilerenderers.classictilerenderer import ClassicTileRenderer
from view.tilerenderers.temperaturetilerenderer import TemperatureTileRenderer
from view.tilerenderers.depthtilerenderer import DepthTileRenderer
from view.tilerenderers.tilerenderer import TileRenderer
from view.tilerenderers.unfilteredterraintilerenderer import UnfilteredTerrainTileRenderer

from view.pixmaputils import PixmapUtils

from parameters import ViewParameters

from model.simulation import Simulation


class Movement(Enum):
    DOWN: int = 0
    UP: int = 1
    RIGHT: int = 2
    LEFT: int = 3


class GraphicalGrid(QGraphicsView):
    tileRenderers = [ClassicTileRenderer,
                     TemperatureTileRenderer, DepthTileRenderer, UnfilteredTerrainTileRenderer]

    def __init__(self, gridSize: Point, grid: Grid, simulation: Simulation, renderingMonitor: RenderMonitor):

        self.luminosityMode = None
        self.simulation = simulation
        self.scene = QGraphicsScene()
        super().__init__(self.scene)

        TileRenderer.setScene(self.scene)

        self.tileRendererIdx: int = 0

        self.latestVerticalValue = renderingMonitor.getFirstYVisible()
        self.latestHorizontalValue = renderingMonitor.getFirstXVisible()
        self.renderingMonitor = renderingMonitor

        self.setMouseTracking(True)

        self.textureSize = ViewParameters.TEXTURE_SIZE
        self.gridSize: Point = gridSize
        self.pixmapItems: List[List[List[TileRenderer]]] = \
            [[[tileRenderer(Point(x, y)) for tileRenderer in self.tileRenderers]
              for x in range(self.gridSize.x())]
             for y in range(self.gridSize.y())]

        for y in range(self.gridSize.y()):
            for x in range(self.gridSize.x()):
                for i in range(len(self.tileRenderers)):
                    if i != self.tileRendererIdx:
                        self.pixmapItems[y][x][i].hide()

        self.initNightMode()

        start_time = time.time()
        self.drawGrid(grid)
        self.initHighlightedTile()
        self.initHook()

        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        # taille de la fenêtre (1000) / grid (100) = 10, divisé par size pixmap
        self.scale(10 / ViewParameters.TEXTURE_SIZE,
                   10 / ViewParameters.TEXTURE_SIZE)

        self.horizontalScrollbar = self.horizontalScrollBar()
        self.verticalScrollbar = self.verticalScrollBar()

        self.horizontalScrollbar.valueChanged.connect(self.horizontalScroll)
        self.verticalScrollbar.valueChanged.connect(self.verticalScroll)

        self.timers: List[List[QTimer, int]] = [[QTimer(), 0, 0] for _ in range(4)]
        self.initTimers()

    def initHighlightedTile(self):
        """
        Initialize the border of the tile to know which tile is selected
        """
        highlight = QPixmap(ViewParameters.HIGHTLIGHTED_TILE_TEXTURE_PATH)
        highlight = highlight.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
        self.highlitedTile = QGraphicsPixmapItem(highlight)
        self.scene.addItem(self.highlitedTile)
        self.chosenEntity = None
        self.highlitedTile.hide()

    def changeTileRenderer(self, newTileRendererIdx: int = None):
        if not newTileRendererIdx:
            newTileRendererIdx = (self.tileRendererIdx + 1) % len(self.tileRenderers)

        for y in range(self.gridSize.y()):
            for x in range(self.gridSize.x()):
                self.pixmapItems[y][x][self.tileRendererIdx].hide()
                self.pixmapItems[y][x][newTileRendererIdx].show()

        self.tileRendererIdx = newTileRendererIdx

        self.drawGrid(self.simulation.getGrid())

        if self.tileRenderers[self.tileRendererIdx].allowsNightCycle():
            self.luminosityMode.show()
        else:
            self.luminosityMode.hide()

    def getPixmapItem(self, point: Point):
        return self.pixmapItems[point.y()][point.x()][self.tileRendererIdx]

    def getCurrentTileRenderer(self) -> Type[TileRenderer]:
        return self.tileRenderers[self.tileRendererIdx]

    def isDefaultTileRenderer(self):
        return self.tileRendererIdx == 0

    def initNightMode(self):
        """
        Initialize a pixmap with the night mode
        """
        self.luminosityMode = QGraphicsPixmapItem(
            PixmapUtils.getPixmapFromRGBHex(ViewParameters.NIGHT_MODE_COLOR))
        self.scene.addItem(self.luminosityMode)
        self.luminosityMode.setPos(0, 0)

        pixmapWidth = self.luminosityMode.pixmap().width()
        sceneWidth, sceneHeight = self.textureSize, self.textureSize

        scale = sceneWidth / pixmapWidth if pixmapWidth > 0 else 1
        transform = QTransform()
        transform.scale(scale * self.gridSize.x(),
                        scale * self.gridSize.y())
        self.luminosityMode.setTransform(transform)
        self.luminosityMode.setOpacity(0.7)

    def updateGrid(self, updatedTiles: Set[Tile]):
        if self.getCurrentTileRenderer().mustNotBeUpdated():
            return

        if not self.getCurrentTileRenderer().mustBeUpdatedAtEveryStep():
            for tile in updatedTiles:
                if tile in self.renderingMonitor.getRenderingSection():
                    self.redraw(tile)
        else:
            self.drawGrid(self.simulation.getGrid())

        self.updateHighlighted()

    def redraw(self, tile: Tile):
        self.getPixmapItem(tile.getPos()).update(tile)

    def updateHighlighted(self):
        if self.chosenEntity and not self.chosenEntity.isDead():
            self._drawHighlightedTile(self.chosenEntity.getTile())
        else:
            self.highlitedTile.hide()

    def drawGrid(self, grid: Grid):
        for tile in grid:
            self.redraw(tile)

    def _drawHighlightedTile(self, tile: Tile):
        x, y = tile.getPos()
        self.highlitedTile.setPos(x * self.textureSize, y * self.textureSize)
        self.highlitedTile.show()

    def removeEntity(self, point: Point):
        assert isinstance(point, Point)
        self.getPixmapItem(point).hideEntity()

    def nightMode(self, hour: int):
        opacity = self.luminosityMode.opacity()
        if hour == ViewParameters.SUNSET_MODE_START:
            self.luminosityMode.setPixmap(
                PixmapUtils.getPixmapFromRGBHex(ViewParameters.SUNSET_MODE_COLOR))
            self.luminosityMode.setOpacity(0.1)
        if hour == ViewParameters.NIGHT_MODE_START:
            self.luminosityMode.setPixmap(
                PixmapUtils.getPixmapFromRGBHex(ViewParameters.NIGHT_MODE_COLOR))
            self.luminosityMode.setOpacity(0.1)
        elif hour == ViewParameters.NIGHT_MODE_FINISH:
            self.luminosityMode.setPixmap(QPixmap())
        elif hour > ViewParameters.NIGHT_MODE_START or hour < ViewParameters.MIDDLE_OF_THE_NIGHT - 2:
            self.luminosityMode.setOpacity(opacity + 0.1)
        elif ViewParameters.MIDDLE_OF_THE_NIGHT + 2 < hour < ViewParameters.NIGHT_MODE_FINISH:
            self.luminosityMode.setOpacity(opacity - 0.1)

    def movePlayer(self, oldPos: Point, newPos: Point):
        self.getPixmapItem(oldPos).hideEntity()
        self.redraw(self.simulation.getGrid().getTile(newPos))
        self.chosenEntity = self.simulation.player
        self.updateHighlighted()

    def removeRenderedSection(self):
        for point in self.renderingMonitor.getRenderingSection():
            self.removeEntity(point)

    def renderSection(self):
        for point in self.renderingMonitor.getRenderingSection():
            self.redraw(self.simulation.getGrid().getTile(point))

    # Redirection of PYQT events to the controller
    def keyPressEvent(self, event):
        GridController.getInstance().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            MainWindowController.getInstance().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        MainWindowController.getInstance().mouseReleaseEvent(event)

    def getVerticalScrollBar(self):
        return self.verticalScrollbar

    def getHorizontalScrollBar(self):
        return self.horizontalScrollbar

    def verticalScroll(self):
        self.removeRenderedSection()
        GridController.getInstance().recomputeCuboid()
        self.renderSection()

    def horizontalScroll(self):
        self.removeRenderedSection()
        GridController.getInstance().recomputeCuboid()
        self.renderSection()

    def moveVerticalScrollBarPositively(self):
        self.moveScrollBar(Movement.DOWN)

    def moveVerticalScrollBarNegatively(self):
        self.moveScrollBar(Movement.UP)

    def moveHorizontalScrollBarPositively(self):
        self.moveScrollBar(Movement.RIGHT)

    def moveHorizontalScrollBarNegatively(self):
        self.moveScrollBar(Movement.LEFT)

    def moveScrollBar(self, movement: Movement):
        if self.timers[movement.value][2] > 1:
            """add time rathenr than reset it when player click too quickly"""
            self.timers[movement.value][1] -= (1000 / 100) * self.renderingMonitor.zoomFactor
            self.timers[movement.value][2] -= 1

        if self.timers[movement.value][1] >= (1000 / 100) * self.renderingMonitor.zoomFactor:
            self.timers[movement.value][0].stop()
            self.timers[movement.value][1] = 0
            self.timers[movement.value][2] = 0
        step = int((1000 / 100) * self.renderingMonitor.zoomFactor / (10 if self.timers[movement.value][1] >= 0 else 5))
        value = step if movement in (Movement.DOWN, Movement.RIGHT) else -step
        if movement in (Movement.UP, Movement.DOWN):
            self.verticalScrollbar.setValue(self.verticalScrollbar.value() + value)
        else:
            self.horizontalScrollbar.setValue(self.horizontalScrollbar.value() + value)
        self.timers[movement.value][1] += step


    def resizeEvent(self, event):
        super().resizeEvent(event)
        GridController.getInstance().resizeEvent(event)

    def initTimers(self):
        for i, (timer, _, _) in enumerate(self.timers):
            timer.setInterval(1)
            match i:
                case Movement.DOWN.value:
                    timer.timeout.connect(self.moveVerticalScrollBarPositively)
                case Movement.UP.value:
                    timer.timeout.connect(self.moveVerticalScrollBarNegatively)
                case Movement.RIGHT.value:
                    timer.timeout.connect(self.moveHorizontalScrollBarPositively)
                case Movement.LEFT.value:
                    timer.timeout.connect(self.moveHorizontalScrollBarNegatively)

    def initSmoothScroll(self, movement: Point):
        # TODO si on appuie trop rapidemment, la caméra ne suivra pas assez bien
        #  solutions : lock du clavier, ou augementer la distance avant la fin du timer à chaque input
        if movement == Point(0, 1):
            self.timers[Movement.DOWN.value][0].start()
            self.timers[Movement.DOWN.value][2] += 1
        elif movement == Point(0, -1):
            self.timers[Movement.UP.value][0].start()
            self.timers[Movement.UP.value][2] += 1
        elif movement == Point(1, 0):
            self.timers[Movement.RIGHT.value][0].start()
            self.timers[Movement.RIGHT.value][2] += 1
        elif movement == Point(-1, 0):
            self.timers[Movement.LEFT.value][0].start()
            self.timers[Movement.LEFT.value][2] += 1

    def setScrollBars(self, point: Point):
        tileSize = int((1000 / 100) * self.renderingMonitor.zoomFactor)
        self.horizontalScrollbar.setValue(point.x() * tileSize)
        self.verticalScrollbar.setValue(point.y() * tileSize)

    def initHook(self):
        hookThrowing = QPixmap(ViewParameters.FISHING_ROD_TEXTURE_PATH)
        hookThrowing = hookThrowing.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
        hook = QPixmap(ViewParameters.HOOK_TEXTURE_PATH)
        hook = hook.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
        fishingRod = QPixmap(ViewParameters.FISHING_ROD_IN_USE_TEXTURE_PATH)
        fishingRod = fishingRod.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
        self.hookedTile = QGraphicsPixmapItem(hook)
        self.hookingPlayer = QGraphicsPixmapItem(fishingRod)
        self.hookThrowing = QGraphicsPixmapItem(hookThrowing)
        self.scene.addItem(self.hookedTile)
        self.scene.addItem(self.hookingPlayer)
        self.scene.addItem(self.hookThrowing)
        self.hookedTile.hide()
        self.hookingPlayer.hide()
        self.hookThrowing.hide()

    def startHooking(self):
        pos = self.simulation.getPlayer().getPos()
        self.hookThrowing.setPos(pos.x() * self.textureSize, pos.y() * self.textureSize)
        self.hookThrowing.show()

    def stopHooking(self):
        self.hookThrowing.hide()

    def drawHook(self, point: Point):
        self.stopHooking()
        pos = self.simulation.getPlayer().getPos()
        self.hookedTile.setPos(point.x() * self.textureSize, point.y() * self.textureSize)
        self.hookingPlayer.setPos(pos.x() * self.textureSize, pos.y() * self.textureSize)

        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(50)
        line = QLineF(int(point.x() * self.textureSize + self.textureSize/2), int(point.y() * self.textureSize + self.textureSize/2),
                         int(pos.x() * self.textureSize + self.textureSize/2), int(pos.y() * self.textureSize) + self.textureSize/2)
        self.line = QGraphicsLineItem(line)
        self.line.setPen(pen)
        self.scene.addItem(self.line)
        self.hookedTile.show()
        self.hookingPlayer.show()
        self.line.show()

    def removeHook(self):
        self.hookedTile.hide()
        self.hookingPlayer.hide()
        self.stopHooking()
        self.scene.removeItem(self.line)
