import time
from typing import Tuple
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from constants import STEP_TIME

from model.simulation import Simulation
from model.renderMonitor import RenderMonitor
from view.graphicalGrid import GraphicalGrid
from controller.gridController import GridController


class Window(QMainWindow):
    def __init__(self, grid_size: Tuple[int, int], simulation: Simulation):
        super().__init__()
        self.setWindowTitle('Simulation 2D')
        self.setGeometry(100, 100, 1000, 1000)
        self.rendering_monitor = simulation.getRenderMonitor()
        self.view = GraphicalGrid(grid_size, simulation.getGrid(), simulation, self.rendering_monitor)
        self.grid_controller = GridController(self.view, simulation, self.rendering_monitor)
        self.setCentralWidget(self.view)
        self.simulation = simulation
        self.total_time = 0
        self.timer = QTimer()
        self.timer.setInterval(STEP_TIME)
        self.timer.timeout.connect(self.recurringTimer)
        self.timer.start()
        self.recurringTimer()

        self.fastF = False
        self.paused = False

        self.layout = QHBoxLayout()
        self.drawButtons()
        self.view.setLayout(self.layout)
        self.setCentralWidget(self.view)

    def pauseTimer(self):

        if self.paused:
            self.paused = False
            self.timer.start()
            self.pauseButton.setStyleSheet(
                "background-color: green; color: white;")

        else:
            self.timer.stop()
            self.paused = True
            self.pauseButton.setStyleSheet(
                "background-color: blue; color: white;")

    def recurringTimer(self):
        self.total_time += 1
        self.simulation.step()
        self.updateGrid()
        self.show_time()

    def show_time(self):
        """
        Display the time passed, one step is one hour
        """

        convert = time.strftime(
            "%A %e:%H hours", time.gmtime(self.total_time * 3600))
        self.timebutton.setText(convert)

    def fastForward(self):
        if self.fastF:
            self.timer.setInterval(STEP_TIME)
            self.fastF = False
            self.fastFbutton.setStyleSheet(
                "background-color: green; color: white;")

        else:
            self.timer.setInterval(STEP_TIME // 2)
            self.fastF = True
            self.fastFbutton.setStyleSheet(
                "background-color: blue; color: white;")

    def getGraphicalGrid(self):
        return self.view

    def updateGrid(self):
        start = time.time()
        self.view.updateGrid(self.simulation.getUpdatedTiles())
        print(f"update time : {time.time() - start}")

    def drawButtons(self):
        self.pauseButton = QPushButton("pause")
        self.pauseButton.setStyleSheet(
            "background-color: green; color: white;")
        self.pauseButton.clicked.connect(self.pauseTimer)

        self.fastFbutton = QPushButton("fast forward")
        self.fastFbutton.setStyleSheet(
            "background-color: green; color: white;")
        self.fastFbutton.clicked.connect(self.fastForward)

        self.timebutton = QPushButton("00:00:00")

        self.layout.addStretch()
        self.layout.addWidget(self.pauseButton)
        self.layout.addWidget(self.fastFbutton)
        self.layout.addWidget(self.timebutton)
        self.layout.addStretch()

        self.layout.setAlignment(self.pauseButton, Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(self.fastFbutton, Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(self.timebutton, Qt.AlignmentFlag.AlignTop)