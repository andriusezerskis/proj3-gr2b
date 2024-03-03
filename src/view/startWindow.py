"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
import threading

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from model.simulation import Simulation
from utils import Point
from view.mainWindow import Window

from view.cssConstants import *

from model.conditionStorage import ConditionStorage


class StartWindow(QMainWindow):
    def __init__(self, storage):
        super().__init__()

        self.storage = storage
        self.mapLoadingThread = threading.Thread(target=self.initMainWindow)
        self.simulation = [None]

        self.setWindowTitle("Deb'île launcher")
        self.setWindowIcon(QIcon("../assets/textures"+"/entities"+"/cow.png"))
        self.setGeometry(100, 100, 100, 100)

        self.setStyleSheet("background-color: #ffd294;") 

        self.layout = QVBoxLayout()
        label = QLabel("Deb'île")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #label.setFont(QFont('Small Fonts', 100)) 
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
        self.spinBoxWidth.setStyleSheet(SPIN_COLOR) 

        self.spinBoxHeight = QSpinBox(minimum=10, maximum=200, value=100)
        self.spinBoxHeight.valueChanged.connect(self.updateSpinboxHeight)
        self.layout2.addWidget(self.spinBoxWidth)
        self.layout2.addWidget(self.spinBoxHeight)
        self.spinBoxHeight.setStyleSheet(SPIN_COLOR)

        # --- Hlayout  ---
        container2 = QWidget()
        container2.setLayout(self.layout2)
        container2.setStyleSheet(HLAYOUT_COLOR)
        self.layout.addWidget(container2)

        label_im = QLabel(self)
        image = QPixmap("../assets/textures"+"/entities"+"/cow.png")
        image = image.scaled(100,100)
        label_im.setPixmap(image)
        label_im.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label_im)

        # ---- ok button ----
        self.button = QPushButton("c parti youpi")
        self.button.clicked.connect(self.startThread)
        self.button.setStyleSheet(START_BUTTON_STYLE_SHEET)
        self.layout.addWidget(self.button)

    def updateSpinboxWidth(self, value):
        self.gridSizeWidth = value

    def updateSpinboxHeight(self, value):
        self.gridSizeHeight = value

    def startThread(self):
        self.mapLoadingThread.start()
        print(f"({threading.get_ident()}) thread created")
        with self.storage.getMapLoadingCondition():
            self.storage.getMapLoadingCondition().wait()
        window = Window(Point(self.gridSizeWidth, self.gridSizeHeight), self.simulation[0], self.storage)
        window.show()
        self.hide()
        # le thread principal ne peut jamais attendre, ni ici ni dans window, le thread ne peut pas dessiner, le seul moyen de ne pas avoir la souris qui freeze -> essayer de dessiner jusqu'à ce qu'on y arrive

    def initMainWindow(self):
        # handler when ok button pressed
        print(f"({threading.get_ident()}) a")
        print(f"({threading.get_ident()}) b")
        self.simulation[0] = Simulation(Point(self.gridSizeWidth, self.gridSizeHeight))
        with self.storage.getMapLoadingCondition():
            self.storage.getMapLoadingCondition().notify()
        print(f"({threading.get_ident()}) c")
