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
        self.setWindowIcon(QIcon("../assets/textures/entities/cow.png"))
        self.setGeometry(100, 100, 100, 100)

        self.setStyleSheet("background-color: #ffd294;")

        self.layout = QVBoxLayout()
        label = QLabel("Deb'île")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # label.setFont(QFont('Small Fonts', 100))
        label.setStyleSheet("QLabel{font-weight: bold}")
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
        self.spinBoxWidth.setStyleSheet(ViewParameters.SPIN_COLOR)

        self.spinBoxHeight = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxHeight.valueChanged.connect(self.updateSpinboxHeight)
        self.layout2.addWidget(self.spinBoxWidth)
        self.layout2.addWidget(self.spinBoxHeight)
        self.spinBoxHeight.setStyleSheet(ViewParameters.SPIN_COLOR)

        # --- Hlayout  ---
        container2 = QWidget()
        container2.setLayout(self.layout2)
        container2.setStyleSheet(ViewParameters.HLAYOUT_COLOR)
        self.layout.addWidget(container2)

        self.loadButton = QPushButton("Charger une carte")
        self.loadButton.setStyleSheet(ViewParameters.BUTTON_STYLESHEET)
        self.loadButton.clicked.connect(self.loadButtonCallback)

        label_im = QLabel(self)
        image = QPixmap("../assets/textures/entities/cow.png")
        image = image.scaled(100, 100)
        label_im.setPixmap(image)
        label_im.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label_im)
        self.layout.addWidget(self.loadButton)

        # ---- ok button ----
        self.button = QPushButton("Commencer !")
        self.button.clicked.connect(self.initMainWindow)
        self.button.setStyleSheet(ViewParameters.START_BUTTON_STYLE_SHEET)
        self.layout.addWidget(self.button)

    def loadButtonCallback(self):
        """
        Callback for the load button
        """
        self.qFileDialog = QFileDialog()
        self.qFileDialog.setNameFilter("Text File (*.*)")
        self.qFileDialog.exec()
        file = self.qFileDialog.selectedFiles()
        self.loadButton.setText("Carte chargée")

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
