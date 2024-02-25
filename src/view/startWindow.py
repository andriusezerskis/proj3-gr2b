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


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        label = QLabel("Deb'île")
        self.layout.addWidget(label)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)
        self.layout2 = QHBoxLayout()

        # ---- input windows size ----
        self.gridSizeWidth = 100
        self.gridSizeHeight = 100
        label2 = QLabel("Taille fenêtre longueur")
        self.layout2.addWidget(label2)
        self.spinBoxWidth = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxWidth.valueChanged.connect(self.updateSpinboxWidth)
        self.spinBoxHeight = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxHeight.valueChanged.connect(self.updateSpinboxHeight)
        self.layout2.addWidget(self.spinBoxWidth)
        self.layout2.addWidget(self.spinBoxHeight)

        # --- Hlayout  ---
        container2 = QWidget()
        container2.setLayout(self.layout2)
        self.layout.addWidget(container2)

        label = QLabel(self)
        pixmap = QPixmap("../assets/textures"+"/entities"+"/cow.png")
        label.setPixmap(pixmap)
        # self.layout.addWidget(label)

        # ---- ok button ----
        self.button = QPushButton("c parti youpi")
        self.button.clicked.connect(self.initMainWindow)
        self.layout.addWidget(self.button)

    def updateSpinboxWidth(self, value):
        self.gridSizeWidth = value

    def updateSpinboxHeight(self, value):
        self.gridSizeHeight = value

    def initMainWindow(self):
        # handler when ok button pressed
        simulation = Simulation(Point(self.gridSizeWidth, self.gridSizeHeight))
        window = Window(
            Point(self.gridSizeWidth, self.gridSizeHeight), simulation)
        window.show()
        self.hide()
