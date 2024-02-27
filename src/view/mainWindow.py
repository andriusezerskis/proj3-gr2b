"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

import time
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QVBoxLayout, QDockWidget, QMainWindow, QPushButton, QWidget, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from constants import MAIN_WINDOW_TITLE, STEP_TIME, TIME_FORMAT
from view.cssConstants import *

from model.entities.entity import Entity
from model.simulation import Simulation

from view.commandsWindow import CommandWindow
from view.graphicalGrid import GraphicalGrid
from view.monitor import GraphWindow, MonitorWindow

from controller.gridController import GridController
from controller.mainWindowController import MainWindowController
from controller.entityInfoController import EntityInfoController


class CustomQDock(QDockWidget):
    def __init__(self, mainWindowController, mainWindow):
        super().__init__("ehhhh", mainWindow)
        self.mainWindowController = mainWindowController
        self.setGeometry(100, 100, 300, 200)
        self.dockLayout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.dockLayout)
        self.setStyleSheet("background-color: #cdc0fb;")
        self.setWidget(container)

    def closeEvent(self, event: QCloseEvent | None) -> None:
        super().closeEvent(event)
        self.mainWindowController.closeDockEvent()


class Window(QMainWindow):
    def __init__(self, gridSize, simulation: Simulation):
        super().__init__()

        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.renderingMonitor = simulation.getRenderMonitor()

        self.view = GraphicalGrid(
            gridSize, simulation.getGrid(), simulation, self.renderingMonitor)
        self.mainWindowController = MainWindowController(
            self.view, simulation, self)
        self.initialiseDock()

        self.gridController = GridController(
            self.view, simulation, self.renderingMonitor)

        self.setCentralWidget(self.view)
        self.simulation = simulation
        self.totalTime = 0

        self.fastF = False
        self.paused = False

        self.layout = QHBoxLayout()
        self.drawButtons()
        self.view.setLayout(self.layout)

        self.initTimer()

        self.commands = CommandWindow(self)

    def initialiseDock(self):
        self.dock = CustomQDock(self.mainWindowController, self)
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        container1 = QWidget()
        container2 = QWidget()
        container3 = QWidget()
        self.dock.dockLayout.addWidget(container1)
        self.dock.dockLayout.addWidget(container3)
        self.dock.dockLayout.addWidget(container2)

        self.monitor = MonitorWindow(self.dock, container1)
        self.graph = GraphWindow(self.dock, container3)
        self.entityController = EntityInfoController(self.dock, container2)

    def initTimer(self):
        self.timer = QTimer()
        self.timer.setInterval(STEP_TIME)
        self.timer.timeout.connect(self.recurringTimer)
        self.timer.start()
        self.recurringTimer()

    def pauseTimer(self):

        if self.paused:
            self.paused = False
            self.timer.start()
            self.pauseButton.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)

        else:
            self.timer.stop()
            self.paused = True
            self.pauseButton.setStyleSheet(CLICKED_BUTTON_STYLESHEET)

    def recurringTimer(self):
        self.totalTime += 1
        self.simulation.step()
        self.updateGrid()
        for i in Entity.__subclasses__():
            for j in i.__subclasses__():
                self.graph.updatePlot(j.getCount(), j)
        self.entityController.update()
        self.showTime()

    def showTime(self):
        """
        Display the time passed, one step is one hour
        """

        convert = time.strftime(
            TIME_FORMAT, time.gmtime(self.totalTime * 3600))
        hour = time.strftime("%H", time.gmtime(self.totalTime * 3600))
        self.timebutton.setText(convert)
        self.view.nightMode(int(hour))

    def fastForward(self):
        if self.fastF:
            self.timer.setInterval(STEP_TIME)
            self.fastF = False
            self.fastFbutton.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)

        else:
            self.timer.setInterval(STEP_TIME // 2)
            self.fastF = True
            self.fastFbutton.setStyleSheet(CLICKED_BUTTON_STYLESHEET)

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
        self.pauseButton.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)
        self.pauseButton.clicked.connect(self.pauseTimer)

        self.fastFbutton = QPushButton("fast forward")
        self.fastFbutton.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)
        self.fastFbutton.clicked.connect(self.fastForward)

        self.timebutton = QPushButton("00:00:00")

        self.commandsButton = QPushButton("Commands")
        self.commandsButton.clicked.connect(self.commandsCallback)

        self.zoomInButton = QPushButton("+")
        self.zoomInButton.clicked.connect(self.gridController.zoomIn)
        self.zoomOutButton = QPushButton("-")
        self.zoomOutButton.clicked.connect(self.gridController.zoomOut)

        self.buttonOpenDock = QPushButton(">")
        self.buttonOpenDock.hide()
        self.buttonOpenDock.clicked.connect(
            self.mainWindowController.openDockEvent)

        self.layout.addWidget(self.buttonOpenDock,
                              alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addStretch()
        self.layout.addWidget(
            self.pauseButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.fastFbutton, alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.timebutton,  alignment=Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(
            self.commandsButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
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
