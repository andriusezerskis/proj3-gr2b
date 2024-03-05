"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from typing import Set, List

from PyQt6.QtCore import QTimer
from controller.gridController import GridController

from utils import Point

from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from model.grid import Grid
from model.terrains.tile import Tile
from model.drawable import ParametrizedDrawable
from model.renderMonitor import RenderMonitor
from model.generator.gridGenerator import GridGenerator

from controller.mainWindowController import MainWindowController

from view.graphicalTile import GraphicalTile


from model.disaster import Disaster

from parameters import ViewParameters

from model.player.player import Player
from model.simulation import Simulation


class GraphicalGrid(QGraphicsView):

    def __init__(self, gridSize: Point, grid: Grid, simulation: Simulation, renderingMonitor: RenderMonitor):
        self.luminosityMode = None
        self.simulation = simulation
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.latestVerticalValue = renderingMonitor.getFirstYVisible()
        self.latestHorizontalValue = renderingMonitor.getFirstXVisible()
        self.renderingMonitor = renderingMonitor

        self.setMouseTracking(True)

        self.texture_size = ViewParameters.TEXTURE_SIZE
        self.gridSize: Point = gridSize
        self.pixmapItems: List[List[GraphicalTile]] = \
            [[GraphicalTile(y, x) for x in range(self.gridSize.x())]
             for y in range(self.gridSize.y())]
        self._addPixmapItems()
        self.pixmapFromPath = {}
        self.pixmapFromRGB = {}

        start_time = time.time()
        self.drawGrid(grid)
        self.initHighlightedTile()

        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        # taille de la fenêtre (1000) / grid (100) = 10, divisé par size pixmap
        self.scale(10 / ViewParameters.TEXTURE_SIZE, 10 / ViewParameters.TEXTURE_SIZE)
        self.initNightMode()

        self.setStyleSheet(ViewParameters.GRID_STYLESHEET)

        self.horizontalScrollbar = self.horizontalScrollBar()
        self.verticalScrollbar = self.verticalScrollBar()

        self.horizontalScrollbar.valueChanged.connect(self.horizontalScroll)
        self.verticalScrollbar.valueChanged.connect(self.verticalScroll)

        self.timers: List[List[QTimer | None | int]] = [
            [None, 0] for _ in range(4)]

    def initHighlightedTile(self):
        """
        Initialize the border of the tile to know which tile is selected
        """
        higlight = QPixmap(ViewParameters.HIGHTLIGHTED_TILE_TEXTURE_PATH)
        higlight.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
        self.highlitedTile = QGraphicsPixmapItem(higlight)
        self.scene.addItem(self.highlitedTile)
        self.chosenEntity = None
        self.highlitedTile.hide()

    def initNightMode(self):
        """
        Initialize a pixmap with the night mode
        """
        self.luminosityMode = QGraphicsPixmapItem(
            self.getPixmapFromRGBHex(ViewParameters.NIGHT_MODE_COLOR))
        self.scene.addItem(self.luminosityMode)
        self.luminosityMode.setPos(0, 0)

        pixmapWidth = self.luminosityMode.pixmap().width()
        sceneWidth, sceneHeight = self.texture_size, self.texture_size

        scale = sceneWidth / pixmapWidth if pixmapWidth > 0 else 1
        transform = QTransform()
        transform.scale(scale * self.gridSize.x(),
                        scale * self.gridSize.y())
        self.luminosityMode.setTransform(transform)
        self.luminosityMode.show()
        self.luminosityMode.setOpacity(0.7)

    def updateGrid(self, updatedTiles: Set[Tile]):
        for tile in updatedTiles:
            if tile in self.renderingMonitor.getRenderingSection():
                self._drawTiles(tile)

        self.updateHighlighted()

    def updateHighlighted(self):
        if self.chosenEntity and not self.chosenEntity.isDead():
            self._drawHighlightedTile(self.chosenEntity.getTile())
        else:
            self.highlitedTile.hide()

    def drawGrid(self, grid: Grid):
        for tile in grid:
            self._drawTiles(tile)

    def _drawTiles(self, tile):
        self._drawTerrains(tile)
        self._drawEntities(tile)
        self._drawDisaster(tile)

    def _drawDisaster(self, tile):
        x, y = tile.getPos()

        if tile.disaster == Disaster.FIRE_TEXT or tile.disaster == Disaster.ICE_TEXT:
            disasterFilter = self.pixmapItems[y][x].getDisasterFilter()
            disasterPixmap = tile.getDisasterPathName()
            disasterFilter.show()
            disasterFilter.setOpacity(tile.disasterOpacity)
            disasterFilter.setPixmap(self.getPixmap(disasterPixmap))

    def _drawTerrains(self, tile):
        x, y = tile.getPos()
        self.pixmapItems[y][x].getTerrain().setPixmap(self.getPixmap(tile))

        # to move in a different spot?
        depthFilter = self.pixmapItems[y][x].getFilter()
        depthFilter.setPixmap(self.getPixmapFromRGBHex(tile.getFilterColor()))

        # linear mapping from 0 <-> X_LEVEL to MAX_FILTER <-> X+1_LEVEL
        levelRange = GridGenerator.getRange(type(tile))
        m = ViewParameters.MAX_TILE_FILTER_OPACITY / (levelRange[1] - levelRange[0])
        p = -levelRange[0] * m
        opacity = m * tile.getHeight() + p

        if not tile.isGradientAscending():
            opacity = ViewParameters.MAX_TILE_FILTER_OPACITY - opacity

        depthFilter.setOpacity(opacity)
        depthFilter.show()

    def _drawEntities(self, tile):
        if tile in self.renderingMonitor.getRenderingSection():
            x, y = tile.getPos()
            if tile.getEntity():
                self.pixmapItems[y][x].getEntity().setPixmap(
                    self.getPixmap(tile.getEntity()))
            else:
                self.pixmapItems[y][x].getEntity().setPixmap(QPixmap())

    def _drawHighlightedTile(self, tile):
        x, y = tile.getPos()
        self.highlitedTile.setPos(x * self.texture_size, y * self.texture_size)
        self.highlitedTile.setScale(1)
        self.highlitedTile.show()

    def removeEntity(self, point: Point):
        assert isinstance(point, Point)
        self.pixmapItems[point.y()][point.x()].getEntity().setPixmap(QPixmap())

    def _removeTerrain(self, point: Point):
        assert isinstance(point, Point)
        self.pixmapItems[point.y()][point.x(
        )].getTerrain().setPixmap(QPixmap())

    def _removeTile(self, point: Point):
        assert isinstance(point, Point)
        self.removeEntity(point)
        self._removeTerrain(point)

    def nightMode(self, hour):
        opacity = self.luminosityMode.opacity()
        if hour == ViewParameters.SUNSET_MODE_START:
            self.luminosityMode.setPixmap(
                self.getPixmapFromRGBHex(ViewParameters.SUNSET_MODE_COLOR))
            self.luminosityMode.setOpacity(0.1)
        if hour == ViewParameters.NIGHT_MODE_START:
            self.luminosityMode.setPixmap(self.getPixmapFromRGBHex(ViewParameters.NIGHT_MODE_COLOR))
            self.luminosityMode.setOpacity(0.1)

        elif hour == ViewParameters.NIGHT_MODE_FINISH:
            self.luminosityMode.setPixmap(QPixmap())
        elif hour > ViewParameters.NIGHT_MODE_START or hour < ViewParameters.MIDDLE_OF_THE_NIGHT - 2:
            self.luminosityMode.setOpacity(opacity + 0.1)
        elif ViewParameters.MIDDLE_OF_THE_NIGHT + 2 < hour < ViewParameters.NIGHT_MODE_FINISH:
            self.luminosityMode.setOpacity(opacity - 0.1)

    def movePlayer(self, oldPos, newPos):
        self.pixmapItems[oldPos.y()][oldPos.x()].getEntity().setPixmap(QPixmap())
        self._drawEntities(self.simulation.getGrid().getTile(newPos))

    def getPixmap(self, graphicalObject: ParametrizedDrawable | str):
        if isinstance(graphicalObject, (ParametrizedDrawable, Player)):
            path = graphicalObject.getTexturePath()
        else:
            path = graphicalObject

        if path not in self.pixmapFromPath:
            # todo print(path)
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(self.texture_size, self.texture_size)
            self.pixmapFromPath[path] = pixmap

        return self.pixmapFromPath[path]

    def getPixmapFromRGBHex(self, rgbHex: str) -> QPixmap:
        if rgbHex not in self.pixmapFromRGB:
            im = QImage(1, 1, QImage.Format.Format_RGB32)
            im.setPixel(0, 0, QColor(rgbHex).rgb())
            pixmap = QPixmap(im)
            pixmap = pixmap.scaled(self.texture_size, self.texture_size)
            self.pixmapFromRGB[rgbHex] = pixmap

        return self.pixmapFromRGB[rgbHex]

    def removeRenderedSection(self):
        for point in self.renderingMonitor.getRenderingSection():
            self.removeEntity(point)

    def renderSection(self):
        for point in self.renderingMonitor.getRenderingSection():
            self._drawTiles(self.simulation.getGrid().getTile(point))

    def _addPixmapItems(self):
        for y, line in enumerate(self.pixmapItems):
            for x, graphicalTile in enumerate(line):
                if Point(x, y) in self.renderingMonitor.getRenderingSection():
                    for label in graphicalTile:
                        self.scene.addItem(label)

    # Redirection of PYQT events to the controller
    def keyPressEvent(self, event):
        GridController.getInstance().keyPressEvent(event)

    def mousePressEvent(self, event):
        MainWindowController.getInstance().mousePressEvent(event)

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
        if self.timers[0][1] >= (1000/100) * self.renderingMonitor.zoomFactor:
            self.timers[0][0].stop()
        step = int((1000/100) * self.renderingMonitor.zoomFactor / 10)
        self.verticalScrollbar.setValue(
            self.verticalScrollbar.value() + step)
        self.timers[0][1] += step

    def moveVerticalScrollBarNegatively(self):
        if self.timers[1][1] >= (1000/100) * self.renderingMonitor.zoomFactor:
            self.timers[1][0].stop()
        step = int((1000/100) * self.renderingMonitor.zoomFactor / 10)
        self.verticalScrollbar.setValue(
            self.verticalScrollbar.value() - step)
        self.timers[1][1] += step

    def moveHorizontalScrollBarPositively(self):
        if self.timers[2][1] >= (1000/100) * self.renderingMonitor.zoomFactor:
            self.timers[2][0].stop()
        step = int((1000/100) * self.renderingMonitor.zoomFactor / 10)
        self.horizontalScrollbar.setValue(
            self.horizontalScrollbar.value() + step)
        self.timers[2][1] += step

    def moveHorizontalScrollBarNegatively(self):
        if self.timers[3][1] >= (1000/100) * self.renderingMonitor.zoomFactor:
            self.timers[3][0].stop()
        step = int((1000/100) * self.renderingMonitor.zoomFactor / 10)
        self.horizontalScrollbar.setValue(
            self.horizontalScrollbar.value() - step)
        self.timers[3][1] += step

    def resizeEvent(self, event):
        super().resizeEvent(event)
        GridController.getInstance().resizeEvent(event)

    def initSmoothScroll(self, movement: Point):
        # TODO si on appuie trop rapidemment, la caméra ne suivra pas assez bien
        #  solutions : lock du clavier, ou augementer la distance avant la fin du timer à chaque input
        timer = QTimer()
        timer.setInterval(1)
        if movement == Point(0, 1):
            self.timers[0] = [timer, 0]
            timer.timeout.connect(self.moveVerticalScrollBarPositively)
        elif movement == Point(0, -1):
            self.timers[1] = [timer, 0]
            timer.timeout.connect(self.moveVerticalScrollBarNegatively)
        elif movement == Point(1, 0):
            self.timers[2] = [timer, 0]
            timer.timeout.connect(self.moveHorizontalScrollBarPositively)
        elif movement == Point(-1, 0):
            self.timers[3] = [timer, 0]
            timer.timeout.connect(self.moveHorizontalScrollBarNegatively)

        timer.start()

    def setScrollBars(self, point: Point):
        tile_size = int((1000/100) * self.renderingMonitor.zoomFactor)
        self.horizontalScrollbar.setValue(point.x() * tile_size)
        self.verticalScrollbar.setValue(point.y() * tile_size)
