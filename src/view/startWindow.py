"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from model.simulation import Simulation
from utils import Point
from view.mainWindow import Window

from parameters import ViewParameters


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deb'île launcher")
        self.setWindowIcon(QIcon("../assets/textures"+"/entities"+"/cow.png"))
        self.setGeometry(0, 0, 1000, 400)

        self.layout = QVBoxLayout()
        label = QLabel("Deb'île")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont('Small Fonts', 80))
        self.layout.addWidget(label)
        container = QWidget()
        container.setLayout(self.layout)
        container.setStyleSheet("background: transparent;")

        self.setObjectName("startWindow")

        self.setCentralWidget(container)
        self.layout2 = QHBoxLayout()

        # ---- input windows size ----
        self.gridSizeWidth = 100
        self.gridSizeHeight = 100
        label2 = QToolButton()
        label2.setText("Taille de la grille")
        label2.setStyleSheet("background: rgba(0,0,0,50);")
        label2.setFixedSize(200, 30)
        self.layout2.addStretch()
        self.layout2.addWidget(label2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.spinBoxWidth = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxWidth.setFixedSize(50, 30)
        self.spinBoxWidth.valueChanged.connect(self.updateSpinboxWidth)
        self.spinBoxWidth.setStyleSheet("background: rgba(0,0,0,50);")

        self.spinBoxHeight = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxHeight.valueChanged.connect(self.updateSpinboxHeight)
        self.spinBoxHeight.setFixedSize(50, 30)
        self.spinBoxHeight.setStyleSheet("background: rgba(0,0,0,50); ")

        self.layout2.addWidget(
            self.spinBoxWidth, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout2.addWidget(
            self.spinBoxHeight, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout2.addStretch()

        # --- Hlayout  ---
        container2 = QWidget()
        container2.setLayout(self.layout2)
        self.layout.addWidget(container2)

        # ---- ok button ----
        self.button = QToolButton()
        self.button.setText("Démarrer")
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(self.initMainWindow)
        self.button.setStyleSheet(ViewParameters.START_BUTTON_STYLE_SHEET)
        self.layout.addWidget(
            self.button, alignment=Qt.AlignmentFlag.AlignCenter)

    def updateSpinboxWidth(self, value: int):
        self.gridSizeWidth = value

    def updateSpinboxHeight(self, value: int):
        self.gridSizeHeight = value

    def initMainWindow(self):
        # handler when ok button pressed
        simulation = Simulation(Point(self.gridSizeWidth, self.gridSizeHeight))
        window = Window(
            Point(self.gridSizeWidth, self.gridSizeHeight), simulation)
        window.show()
        self.hide()
