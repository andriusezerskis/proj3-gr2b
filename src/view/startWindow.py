"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from model.generator.entitiesGenerator import EntitiesGenerator
from model.generator.gridGenerator import GridGenerator
from model.grid import Grid
from model.gridloader import GridLoader

from model.simulation import Simulation
from utils import Point
from view.mainWindow import Window

from parameters import ViewParameters


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation")
        self.setWindowIcon(QIcon("../assets/textures"+"/entities"+"/cow.png"))
        self.setGeometry(0, 0, 1000, 400)

        self.layout = QVBoxLayout()
        label = QLabel("Simulation")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont('Small Fonts', 80))
        label.setObjectName("Transparent")
        self.layout.addWidget(label)
        container = QWidget()
        container.setLayout(self.layout)
        container.setObjectName("Transparent")

        self.setObjectName("startWindow")

        self.setCentralWidget(container)
        self.layout2 = QHBoxLayout()
        self.file = None

        # ---- input windows size ----
        self.gridSizeWidth = 100
        self.gridSizeHeight = 100
        label2 = QToolButton()
        label2.setText("Taille de la grille")
        label2.setObjectName("semiTransparent")
        label2.setFixedSize(200, 30)
        self.layout2.addStretch()
        self.layout2.addWidget(label2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.spinBoxWidth = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxWidth.setFixedSize(50, 30)
        self.spinBoxWidth.valueChanged.connect(self.updateSpinboxWidth)
        self.spinBoxWidth.setObjectName("semiTransparent")

        self.spinBoxHeight = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxHeight.valueChanged.connect(self.updateSpinboxHeight)
        self.spinBoxHeight.setFixedSize(50, 30)
        self.spinBoxHeight.setObjectName("semiTransparent")

        self.layout2.addWidget(
            self.spinBoxWidth, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout2.addWidget(
            self.spinBoxHeight, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout2.addStretch()

        self.loadButton = QToolButton()
        self.loadButton.setText("Charger une carte")
        self.loadButton.clicked.connect(self.loadButtonCallback)
        self.loadButton.setFixedSize(200, 30)
        self.loadButton.setObjectName("semiTransparent")

        # --- Hlayout  ---
        container2 = QWidget()
        container2.setLayout(self.layout2)
        container2.setObjectName("Transparent")
        self.layout.addWidget(container2)
        self.layout.addWidget(
            self.loadButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # ---- ok button ----
        self.button = QToolButton()
        self.button.setText("Démarrer")
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(self.initMainWindow)
        self.button.setObjectName("startButton")
        self.layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter)

    def loadButtonCallback(self):
        """
        Callback for the load button
        """
        self.qFileDialog = QFileDialog()
        self.qFileDialog.setNameFilter("MAP files (*.map)")
        self.qFileDialog.exec()
        self.file = self.qFileDialog.selectedFiles()
        if self.file and self.file[0].endswith(".map"):
            self.loadButton.setText("Carte chargée")
            # desactivate the button to choose the size of the map
            self.spinBoxWidth.setEnabled(False)
            self.spinBoxHeight.setEnabled(False)

    def updateSpinboxWidth(self, value: int):
        self.gridSizeWidth = value

    def updateSpinboxHeight(self, value: int):
        self.gridSizeHeight = value

    def initMainWindow(self):
        if not self.file or not self.file[0].endswith(".map"):
            self.grid = GridGenerator(Point(self.gridSizeWidth, self.gridSizeHeight), [
                                      2, 3, 4, 5, 6], 350).generateGrid()
            EntitiesGenerator().generateEntities(self.grid)
        else:
            self.grid = GridLoader.loadFromFile(self.file[0])

        simulation = Simulation(
            self.grid.gridSize, self.grid)
        window = Window(
            self.grid.gridSize, simulation)
        window.show()
        self.hide()
