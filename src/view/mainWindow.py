"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from parameters import ViewParameters, ViewText
from utils import Point, getTerminalSubclassesOfClass

from model.entities.entity import Entity
from model.simulation import Simulation
from model.gridexporter import GridExporter

from view.commandsWindow import CommandWindow
from view.graphicalGrid import GraphicalGrid

from controller.gridController import GridController
from controller.mainWindowController import MainWindowController

from view.docksMonitor import DocksMonitor


class Window(QMainWindow):
    def __init__(self, gridSize: Point, simulation: Simulation):
        super().__init__()

        self.setWindowTitle(ViewText.MAIN_WINDOW_TITLE)
        self.renderingMonitor = simulation.getRenderMonitor()

        self.view = GraphicalGrid(
            gridSize, simulation.getGrid(), simulation, self.renderingMonitor)
        self.mainWindowController = MainWindowController(
            self.view, simulation, self)
        self.layout = QHBoxLayout()
        self.drawButtons()
        self.docksMonitor = DocksMonitor(self.mainWindowController, self)

        self.gridController = GridController(
            self.view, simulation, self.renderingMonitor)

        self.setCentralWidget(self.view)
        self.simulation = simulation
        self.totalTime = 0

        self.fastF = False
        self.paused = False

        self.drawButtons2()
        self.view.setLayout(self.layout)

        self.initTimer()

        self.commands = CommandWindow(self)

    def initTimer(self):
        self.timer = QTimer()
        self.timer.setInterval(ViewParameters.STEP_TIME)
        self.timer.timeout.connect(self.recurringTimer)
        self.timer.start()
        self.recurringTimer()

    def pauseTimer(self):

        if self.paused:
            self.paused = False
            self.timer.start()

        else:
            self.timer.stop()
            self.paused = True

    def recurringTimer(self):
        self.totalTime += 1
        self.simulation.step()
        self.updateGrid()
        for j in getTerminalSubclassesOfClass(Entity):
            self.docksMonitor.getCurrentDock().updateContent(j)
        self.docksMonitor.getCurrentDock().updateController()
        self.showTime()

    def showTime(self):
        """
        Display the time passed, one step is one hour
        """
        convert = time.strftime(
            ViewParameters.TIME_FORMAT, time.gmtime(self.totalTime * 3600))
        nb_days = self.totalTime // 24 + 1
        hour = self.totalTime % 24
        #hour = time.strftime("%-H", time.gmtime(self.totalTime * 3600))
        if int(hour) == ViewParameters.NIGHT_MODE_START:
            self.timebutton.setIcon(QIcon(ViewParameters.MOON_ICON))
        elif int(hour) == ViewParameters.NIGHT_MODE_FINISH:
            self.timebutton.setIcon(QIcon(ViewParameters.SUN_ICON))
        self.timebutton.setText(f"Jour {nb_days} - {"0" if hour < 10 else ""}{hour}h")
        self.view.nightMode(int(hour))

    def fastForward(self):
        if self.fastF:
            self.timer.setInterval(ViewParameters.STEP_TIME)
            self.fastF = False

        else:
            self.timer.setInterval(ViewParameters.STEP_TIME // 2)
            self.fastF = True

    def changeTileRenderer(self):
        if not self.simulation.hasPlayer():
            self.view.changeTileRenderer()
            self.view.chosenEntity = None
            self.view.updateHighlighted()
            self.docksMonitor.getCurrentDock().entityController.view.deselectEntity()

    def saveGrid(self):
        GridExporter.exportToMap(self.getGraphicalGrid().simulation.getGrid())
        print("Saved grid !")

    def getGraphicalGrid(self):
        return self.view

    def updateGrid(self):
        """
        Update the grid with the tiles that has been updated by the simulation
        """
        start = time.time()
        self.view.updateGrid(self.simulation.getUpdatedTiles())
        print(f"update time : {time.time() - start}")

    def commandsCallback(self):
        self.commands.show()

    def drawButtons(self):
        self.pauseButton = QPushButton("⏸︎")
        self.pauseButton.setCheckable(True)
        self.pauseButton.clicked.connect(self.pauseTimer)

        self.fastFbutton = QPushButton("⏩")
        self.fastFbutton.setCheckable(True)
        self.fastFbutton.clicked.connect(self.fastForward)

        self.timebutton = QPushButton("00:00:00")
        self.timebutton.setIcon(QIcon(ViewParameters.MOON_ICON))

        #self.commandsButton = QPushButton("Commands")
        #self.commandsButton.clicked.connect(self.commandsCallback)

        self.changeTileRendererButton = QPushButton("Changer de rendu")
        self.changeTileRendererButton.clicked.connect(self.changeTileRenderer)

        self.saveGridButton = QPushButton("Sauvegarder")
        self.saveGridButton.clicked.connect(self.saveGrid)

        self.buttonOpenDock = QPushButton("⇨")
        self.buttonOpenDock.hide()
        self.buttonOpenDock.clicked.connect(
            self.mainWindowController.openDockEvent)

        self.layout.addWidget(self.buttonOpenDock,
                              alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.addStretch()
        self.layout.addWidget(
            self.pauseButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.fastFbutton, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.timebutton,  alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.changeTileRendererButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.saveGridButton, alignment=Qt.AlignmentFlag.AlignTop)
        """self.layout.addWidget(
            self.commandsButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)"""

    def drawButtons2(self):
        self.zoomInButton = QPushButton("+")
        self.zoomInButton.clicked.connect(self.gridController.zoomIn)
        self.zoomOutButton = QPushButton("-")
        self.zoomOutButton.clicked.connect(self.gridController.zoomOut)
        MainWindowController.getInstance().onZoomIn()
        MainWindowController.getInstance().onZoomOut()
        self.layout.addWidget(
            self.zoomInButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(
            self.zoomOutButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.layout.addStretch()

    def closeEvent(self, event):
        self.pauseTimer()
        result = QMessageBox.question(
            self, "Confirmer la fermeture...", "Êtes-vous sûr de vouloir fermer la fenêtre ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        event.ignore()

        if result == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            self.pauseTimer()
            event.ignore()
