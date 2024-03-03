"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QTimer
# <<<<<<< HEAD
# from constants import MAIN_WINDOW_TITLE, STEP_TIME, TIME_FORMAT
from view.cssConstants import *
# =======

from parameters import ViewParameters, ViewText
#>>>>>>> 7b4187af9561509892ff2ba449d4fe9c0c6259c5

from model.entities.entity import Entity
from model.simulation import Simulation

from view.commandsWindow import CommandWindow
from view.graphicalGrid import GraphicalGrid

from controller.gridController import GridController
from controller.mainWindowController import MainWindowController

from view.docksMonitor import DocksMonitor


class Window(QMainWindow):
    def __init__(self, gridSize, simulation: Simulation):
        super().__init__()

        self.setWindowTitle(ViewText.MAIN_WINDOW_TITLE)
        self.renderingMonitor = simulation.getRenderMonitor()

        self.view = GraphicalGrid(gridSize, simulation.getGrid(), simulation, self.renderingMonitor)
        self.mainWindowController = MainWindowController(self.view, simulation, self)
        self.layout = QHBoxLayout()
        self.drawButtons()
        self.docksMonitor = DocksMonitor(self.mainWindowController, self)

        self.gridController = GridController(self.view, simulation, self.renderingMonitor)

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
            self.pauseButton.setStyleSheet(ViewParameters.NOT_CLICKED_BUTTON_STYLESHEET)

        else:
            self.timer.stop()
            self.paused = True
            self.pauseButton.setStyleSheet(ViewParameters.CLICKED_BUTTON_STYLESHEET)

    def recurringTimer(self):
        self.totalTime += 1
        self.simulation.calculate_step()
        """with self.simulation.viewUpdateCondition:
            self.simulation.viewUpdateCondition.wait()"""
        self.updateGrid()
        for i in Entity.__subclasses__():
            for j in i.__subclasses__():
                self.docksMonitor.getCurrentDock().updateContent(j)
        self.docksMonitor.getCurrentDock().updateController()
        self.showTime()

    def showTime(self):
        """
        Display the time passed, one step is one hour
        """

        convert = time.strftime(
            ViewParameters.TIME_FORMAT, time.gmtime(self.totalTime * 3600))
        hour = time.strftime("%H", time.gmtime(self.totalTime * 3600))
        self.timebutton.setText(convert)
        self.view.nightMode(int(hour))

    def fastForward(self):
        if self.fastF:
            self.timer.setInterval(ViewParameters.STEP_TIME)
            self.fastF = False
            self.fastFbutton.setStyleSheet(ViewParameters.NOT_CLICKED_BUTTON_STYLESHEET)

        else:
            self.timer.setInterval(ViewParameters.STEP_TIME // 2)
            self.fastF = True
            self.fastFbutton.setStyleSheet(ViewParameters.CLICKED_BUTTON_STYLESHEET)

    def getGraphicalGrid(self):
        return self.view

    def updateGrid(self):
        start = time.time()
        self.view.updateGrid(self.simulation.getUpdatedTiles())
        print(f"update time : {time.time() - start}")

    def commandsCallback(self):
        self.commands.show()

    def drawButtons(self):
        self.pauseButton = QPushButton("pause")
        self.pauseButton.setStyleSheet(ViewParameters.NOT_CLICKED_BUTTON_STYLESHEET)
        self.pauseButton.clicked.connect(self.pauseTimer)

        self.fastFbutton = QPushButton("fast forward")
        self.fastFbutton.setStyleSheet(ViewParameters.NOT_CLICKED_BUTTON_STYLESHEET)
        self.fastFbutton.clicked.connect(self.fastForward)

        self.timebutton = QPushButton("00:00:00")

        self.commandsButton = QPushButton("Commands")
        self.commandsButton.clicked.connect(self.commandsCallback)

        self.buttonOpenDock = QPushButton(">")
        self.buttonOpenDock.hide()
        self.buttonOpenDock.clicked.connect(self.mainWindowController.openDockEvent)

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
            self.commandsButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


    def drawButtons2(self):
        self.zoomInButton = QPushButton("+")
        self.zoomInButton.clicked.connect(self.gridController.zoomIn)
        self.zoomOutButton = QPushButton("-")
        self.zoomOutButton.clicked.connect(self.gridController.zoomOut)
        self.layout.addWidget(
            self.zoomInButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(
            self.zoomOutButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.layout.addStretch()

    def closeEvent(self, event):
        result = QMessageBox.question(
            self, "Confirm Exit...", "Are you sure you want to exit ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        event.ignore()

        if result == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
