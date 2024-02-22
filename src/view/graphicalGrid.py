"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from typing import Tuple, Set, List

from PyQt6.QtCore import QTimer
from controller.gridController import GridController

from utils import Point, Point3D

from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from math import sin, sqrt

from model.grid import Grid
from model.terrains.tile import Tile
from model.terrains.tiles import Water
from model.drawable import ParametrizedDrawable
from model.renderMonitor import RenderMonitor
from model.renderMonitor import Cuboid
from model.generator.gridGenerator import GridGenerator

from controller.mainWindowController import MainWindowController

from view.graphicalTile import GraphicalTile

from constants import FIRE, NIGHT_MODE, SUNSET_MODE_START, SUNSET_MODE, NIGHT_MODE_START, NIGHT_MODE_FINISH, \
    MIDDLE_OF_THE_NIGHT, HIGHLIGHTED_TILE, MAX_TILE_FILTER_OPACITY
from src.model.simulation import Simulation


class GraphicalGrid(QGraphicsView):

    def __init__(self, grid_size: Tuple[int, int], grid: Grid, simulation: Simulation, renderingMonitor: RenderMonitor):
        self.luminosityMode = None
        self.simulation = simulation
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.latestVerticalValue = renderingMonitor.getFirstYVisible()
        self.latestHorizontalValue = renderingMonitor.getFirstXVisible()
        self.renderingMonitor = renderingMonitor

        self.setMouseTracking(True)

        self.size = 2048, 2048
        self.gridSize = grid_size
        self.pixmapItems: List[List[GraphicalTile]] = \
            [[GraphicalTile(i, j) for j in range(self.gridSize[0])]
             for i in range(self.gridSize[1])]
        self._addPixmapItems()
        self.pixmapFromPath = {}
        self.pixmapFromRGB = {}
        self.sunPos = Point3D(self.gridSize[0] / 2, -50, 2)

        start_time = time.time()
        self.drawGrid(grid)
        self.initHighlightedTile()

        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        # taille de la fenêtre (1000) / grid (100) = 10, divisé par size pixmap
        self.scale(10 / 2048, 10 / 2048)
        # self.scene.moveToThread()
        # self.initNightMode()

        self.changeStyleSheet()

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
        self.highlitedTile = QGraphicsPixmapItem(QPixmap(HIGHLIGHTED_TILE))
        self.scene.addItem(self.highlitedTile)
        self.chosenEntity = None
        self.highlitedTile.hide()

    def changeStyleSheet(self):
        self.setStyleSheet("""
            QScrollBar:horizontal {
                background-color: #808080; /* Couleur de fond */
                height: 15px; /* Hauteur */
            }

            QScrollBar::handle:horizontal {
                background-color: #C0C0C0; /* Couleur du curseur */
                min-width: 50px; /* Largeur minimale */
            }

            QScrollBar::add-line:horizontal {
                background: none;
            }

            QScrollBar::sub-line:horizontal {
                background: none;
            }

            QScrollBar:vertical {
                background-color: #808080; /* Couleur de fond */
                width: 15px; /* Largeur */
            }

            QScrollBar::handle:vertical {
                background-color: #C0C0C0; /* Couleur du curseur */
                min-height: 50px; /* Hauteur minimale */
            }

            QScrollBar::add-line:vertical {
                background: none;
            }

            QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

    def initNightMode(self):
        """
        Initialize a pixmap with the night mode
        """
        self.luminosityMode = QGraphicsPixmapItem(self.getPixmapFromRGBHex(NIGHT_MODE))
        self.scene.addItem(self.luminosityMode)
        self.luminosityMode.setPos(0, 0)

        pixmapWidth = self.luminosityMode.pixmap().width()
        sceneWidth, sceneHeight = self.size

        scale = sceneWidth / pixmapWidth if pixmapWidth > 0 else 1
        self.luminosityMode.setScale(scale * self.gridSize[0])
        self.luminosityMode.show()
        self.luminosityMode.setOpacity(0.7)

    def updateGrid(self, updatedTiles: Set[Tile]):
        for tile in updatedTiles:
            if tile.getIndex() in self.renderingMonitor.getRenderingSection():
                self._drawTiles(tile)

        self.updateHighlighted()

    def _updateSunlight(self, tile: Tile):
        maxt = 100
        # if tile.getPos() != Point(10, 10):
        #     return
        tilePos3D = Point3D(tile.getPos().x(), tile.getPos().y(), tile.height)

        # the equations of the line from the sun to tile (t in [0; maxt]):
        # x = lambda t: (self.sunPos.x() - tilePos3D.x()) / maxt * t + tilePos3D.x()
        # y = lambda t: (self.sunPos.y() - tilePos3D.y()) / maxt * t + tilePos3D.y()
        # z = lambda t: self.sunPos.x() / maxt * t

        # simplification
        # find all intersections of this line on all lines from tile.y() to 0 on the x axis
        # then, we get the highest tile of these
        highest = None
        for y in range(tile.getPos().y() - 1, -1, -1):
            t = (y - tilePos3D.y()) * maxt / (self.sunPos.y() - tilePos3D.y())
            x = (self.sunPos.x() - tilePos3D.x()) / maxt * t + tilePos3D.x()
            currentTile = self.simulation.getGrid().getTile(Point(round(x), y))
            if not highest or currentTile.height > highest.height:
                highest = currentTile

        # depthFilter = self.pixmapItems[tile.getPos().x()][tile.getPos().x()].getFilter()
        # depthFilter.setPixmap(self.getPixmapFromRGBHex("#00ffff"))
        # depthFilter.setOpacity(1)
        # depthFilter.show()
        #
        # depthFilter = self.pixmapItems[highest.getPos().y()][highest.getPos().x()].getFilter()
        # depthFilter.setPixmap(self.getPixmapFromRGBHex("#ff0000"))
        # depthFilter.setOpacity(1)
        # depthFilter.show()

        # i cannot make this work
        # angle = (Point3D(highest.getPos().x(), highest.getPos().y(), highest.height) - tilePos3D)
        # .angle(self.sunPos - tilePos3D)

        angle = -1
        if highest and highest.height > Water.getLevel() and self.sunPos.z() > 0 and highest.height < self.sunPos.z():

            angleHighest = (Point3D(highest.getPos().x(), highest.getPos().y(), 0) -
                            Point3D(tile.getPos().x(), tile.getPos().y(), 0)).angle(
                Point3D(highest.getPos().x(), highest.getPos().y(), highest.height) - tilePos3D)

            angleSun = (Point3D(self.sunPos.x(), self.sunPos.y(), 0) -
                        Point3D(tile.getPos().x(), tile.getPos().y(), 0)).angle(self.sunPos - tilePos3D)

            angle = angleSun - angleHighest

        solarFilter = self.pixmapItems[tile.getPos().y()][tile.getPos().x()].getSolarFilter()

        # print(f"height of tile to shade: {tile.height}")
        # print(f"height of potentially shading tile: {highest.height}")
        # print(f"vector from tile to potential shading tile: "
        #       f"{Point3D(highest.getPos().x(), highest.getPos().y(), highest.height) - tilePos3D}")
        # print(f"vector from tile to sun: {self.sunPos - tilePos3D}")
        # print(f"angle between the two {angle} rad")

        sunny = True
        if not highest:
            sunny = self.sunPos.z() > 0
        else:
            sunny = (self.sunPos.z() > 0 and ((angle > 0 and highest.height < self.sunPos.z()) or
                                              highest.height < Water.getLevel() or tile.height > highest.height))

        if sunny:
            solarFilter.hide()
        else:
            solarFilter.setPixmap(self.getPixmapFromRGBHex(NIGHT_MODE))

            scale = 1
            if highest:
                scale = 1 / highest.getPos().euclidDistance(tile.getPos())
            print(self.sunPos.z() / sqrt(self.sunPos.z()**2 + self.sunPos.y()**2))
            solarFilter.setOpacity(0.7 - 6 * self.sunPos.z() / sqrt(self.sunPos.z()**2 + self.sunPos.y()**2))
            solarFilter.show()

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
        self._updateSunlight(tile)

    def _drawDisaster(self, tile):
        i, j = tile.getIndex()

        if tile.disaster != None:
            disasterFilter = self.pixmapItems[i][j].getDisasterFilter()
            disasterFilter.show()
            disasterFilter.setOpacity(tile.disasterOpacity)
            disasterFilter.setPixmap(self.getPixmap(FIRE))

    def _drawTerrains(self, tile):
        i, j = tile.getIndex()
        self.pixmapItems[i][j].getTerrain().setPixmap(self.getPixmap(tile))

        # to move in a different spot?
        depthFilter = self.pixmapItems[i][j].getFilter()
        depthFilter.setPixmap(self.getPixmapFromRGBHex(tile.getFilterColor()))

        # linear mapping from 0 <-> X_LEVEL to MAX_FILTER <-> X+1_LEVEL
        levelRange = GridGenerator.getRange(type(tile))
        m = MAX_TILE_FILTER_OPACITY / (levelRange[1] - levelRange[0])
        p = -levelRange[0] * m
        opacity = m * tile.getHeight() + p

        if not tile.isGradientAscending():
            opacity = MAX_TILE_FILTER_OPACITY - opacity

        depthFilter.setOpacity(opacity)
        depthFilter.show()

    def _drawEntities(self, tile):
        if tile in self.renderingMonitor.getRenderingSection():
            i, j = tile.getIndex()
            if tile.getEntity():
                self.pixmapItems[i][j].getEntity().setPixmap(
                    self.getPixmap(tile.getEntity()))
            else:
                self.pixmapItems[i][j].getEntity().setPixmap(QPixmap())

    def _drawHighlightedTile(self, tile):
        i, j = tile.getIndex()
        self.highlitedTile.setPos(j * 2048, i * 2048)
        self.highlitedTile.setScale(1)
        self.highlitedTile.show()

    def removeEntity(self, i, j):
        self.pixmapItems[i][j].getEntity().setPixmap(QPixmap())

    def _removeTerrain(self, i, j):
        self.pixmapItems[i][j].getTerrain().setPixmap(QPixmap())

    def _removeTile(self, i, j):
        self.removeEntity(i, j)
        self._removeTerrain(i, j)

    def moveCamera(self, cuboids: Tuple[Cuboid, Cuboid]):
        lost, won = cuboids
        for i, j in lost:
            self.pixmapItems[i][j].DisableEntityRendering()
            self.pixmapItems[i][j].getEntity().setPixmap(QPixmap())
        for i, j in won:
            self.pixmapItems[i][j].EnableEntityRendering()
            self._drawTiles(self.simulation.getGrid().getTile(Point(j, i)))

    def nightMode(self, hour):
        return

        opacity = self.luminosityMode.opacity()
        if hour == SUNSET_MODE_START:
            self.luminosityMode.setPixmap(self.getPixmapFromRGBHex(SUNSET_MODE))
            self.luminosityMode.setOpacity(0.1)
        if hour == NIGHT_MODE_START:
            self.luminosityMode.setPixmap(self.getPixmapFromRGBHex(NIGHT_MODE))
            self.luminosityMode.setOpacity(0.1)

        elif hour == NIGHT_MODE_FINISH:
            self.luminosityMode.setPixmap(QPixmap())
        elif hour > NIGHT_MODE_START or hour < MIDDLE_OF_THE_NIGHT - 2:
            self.luminosityMode.setOpacity(opacity + 0.1)
        elif MIDDLE_OF_THE_NIGHT + 2 < hour < NIGHT_MODE_FINISH:
            self.luminosityMode.setOpacity(opacity - 0.1)

    def movePlayer(self, old_pos, new_pos):
        i, j = old_pos.y(), old_pos.x()
        self.pixmapItems[i][j].getEntity().setPixmap(QPixmap())
        self._drawEntities(self.simulation.getGrid().getTile(new_pos))

    def getPixmap(self, graphicalObject: ParametrizedDrawable | str):
        if isinstance(graphicalObject, ParametrizedDrawable):
            path = graphicalObject.getTexturePath()
        else:
            path = graphicalObject

        if path not in self.pixmapFromPath:
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmapFromPath[path] = pixmap

        return self.pixmapFromPath[path]

    def getPixmapFromRGBHex(self, rgbHex: str) -> QPixmap:
        if rgbHex not in self.pixmapFromRGB:
            im = QImage(1, 1, QImage.Format.Format_RGB32)
            im.setPixel(0, 0, QColor(rgbHex).rgb())
            pixmap = QPixmap(im)
            pixmap = pixmap.scaled(self.size[0], self.size[1])
            self.pixmapFromRGB[rgbHex] = pixmap

        return self.pixmapFromRGB[rgbHex]

    def removeRenderedSection(self):
        for i, j in self.renderingMonitor.getRenderingSection():
            self._removeTile(i, j)

    def renderSection(self):
        for i, j in self.renderingMonitor.getRenderingSection():
            self._drawTiles(self.simulation.getGrid().getTile(Point(j, i)))

    def _addPixmapItems(self):
        for i, line in enumerate(self.pixmapItems):
            for j, graphicalTile in enumerate(line):
                if (i, j) in self.renderingMonitor.getRenderingSection() and self.simulation.getGrid().getTile(
                        Point(j, i)).hasEntity():
                    graphicalTile.EnableEntityRendering()
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
        if self.timers[0][1] >= (1000 / 100) * self.renderingMonitor.zoomFactor:
            self.timers[0][0].stop()
        step = int((1000 / 100) * self.renderingMonitor.zoomFactor / 10)
        self.verticalScrollbar.setValue(
            self.verticalScrollbar.value() + step)
        self.timers[0][1] += step

    def moveVerticalScrollBarNegatively(self):
        if self.timers[1][1] >= (1000 / 100) * self.renderingMonitor.zoomFactor:
            self.timers[1][0].stop()
        step = int((1000 / 100) * self.renderingMonitor.zoomFactor / 10)
        self.verticalScrollbar.setValue(
            self.verticalScrollbar.value() - step)
        self.timers[1][1] += step

    def moveHorizontalScrollBarPositively(self):
        if self.timers[2][1] >= (1000 / 100) * self.renderingMonitor.zoomFactor:
            self.timers[2][0].stop()
        step = int((1000 / 100) * self.renderingMonitor.zoomFactor / 10)
        self.horizontalScrollbar.setValue(
            self.horizontalScrollbar.value() + step)
        self.timers[2][1] += step

    def moveHorizontalScrollBarNegatively(self):
        if self.timers[3][1] >= (1000 / 100) * self.renderingMonitor.zoomFactor:
            self.timers[3][0].stop()
        step = int((1000 / 100) * self.renderingMonitor.zoomFactor / 10)
        self.horizontalScrollbar.setValue(
            self.horizontalScrollbar.value() - step)
        self.timers[3][1] += step

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
        tile_size = int((1000 / 100) * self.renderingMonitor.zoomFactor)
        self.horizontalScrollbar.setValue(point.x() * tile_size)
        self.verticalScrollbar.setValue(point.y() * tile_size)
