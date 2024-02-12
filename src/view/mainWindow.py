import time
from typing import Tuple
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from constants import *

from model.entities.human import Human
from model.simulation import Simulation

from view.graphicalGrid import GraphicalGrid
from view.entityInfoView import EntityInfoView
from view.monitor import MonitorWindow

from controller.mainWindowController import MainWindowController



class CommandWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CommandWindow, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.setWindowTitle(COMMANDS_WINDOW_TITLE)

        self.central_widget: QWidget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.createCommands()

    def createCommands(self):
        self.firstCommand = QLabel(MOVE_CAMERA_UP)
        self.layout.addWidget(self.firstCommand)


class Window(QMainWindow):
    def __init__(self, grid_size: Tuple[int, int], simulation: Simulation):
        super().__init__()
        self.setWindowTitle(MAIN_WINDOW_TITLE)
        self.rendering_monitor = simulation.getRenderMonitor()
        self.dockDebile = MonitorWindow("Monitor deb'île", self)
        self.dock2 = EntityInfoView("Entity Info", self)

        self.view = GraphicalGrid(
            grid_size, simulation.getGrid(), simulation, self.rendering_monitor)
        self.grid_controller = MainWindowController(
            self.view, simulation, self.rendering_monitor, self)
        self.setCentralWidget(self.view)
        self.simulation = simulation
        self.total_time = 0

        self.fastF = False
        self.paused = False

        self.layout = QHBoxLayout()
        self.drawButtons()
        self.view.setLayout(self.layout)

        self.initTimer()

        self.commands = CommandWindow(self)
        self.showMaximized()
        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea, self.dockDebile)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock2)

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
        self.dockDebile.getGraph().updatePlot(
            Human.count)
        self.dock2.updateOnStep()
        # yo deso demeter mais on reglera le probleme plus tard
        self.show_time()

    def show_time(self):
        """
        Display the time passed, one step is one hour
        """

        convert = time.strftime(
            "%A %e:%H hours", time.gmtime(self.total_time * 3600))
        hour = time.strftime("%H", time.gmtime(self.total_time * 3600))
        self.timebutton.setText(convert)
        self.view.nightMode(int(hour))

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

    def commandsCallback(self):
        self.commands.show()

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

        self.commandsButton = QPushButton("Commands")
        self.commandsButton.clicked.connect(self.commandsCallback)

        self.layout.addStretch()
        self.layout.addWidget(self.pauseButton)
        self.layout.addWidget(self.fastFbutton)
        self.layout.addWidget(self.timebutton)
        self.layout.addWidget(self.commandsButton)
        self.layout.addStretch()

        self.layout.setAlignment(self.pauseButton, Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(self.fastFbutton, Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(self.timebutton, Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(
            self.commandsButton, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
