import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from model.simulation import Simulation
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

        self.layout_2 = QHBoxLayout()

        # ---- taille fenetre ----
        self.size = 100
        label_2 = QLabel("Taille fenêtre longueur")
        self.layout_2.addWidget(label_2)
        self.spin_box = QSpinBox(minimum=10, maximum=200, value=100)
        self.spin_box.valueChanged.connect(self.update_spinbox)
        self.layout_2.addWidget(self.spin_box)

        # --- ajout layout H ---
        container_2 = QWidget()
        container_2.setLayout(self.layout_2)
        self.layout.addWidget(container_2)

        # miaou
        label = QLabel(self)
        pixmap = QPixmap("../assets/textures"+"/entities"+"/cow.png")
        label.setPixmap(pixmap)
        # self.layout.addWidget(label)

        # ---- bouton OK ----
        self.button = QPushButton("c parti youpi")
        self.button.clicked.connect(self.initMainWindow)
        self.layout.addWidget(self.button)

    def update_spinbox(self, value):
        self.size = value

    def initMainWindow(self):
        # handler de oke bouton
        print('lol')

        simulation = Simulation((self.size, self.size))
        window = Window((self.size, self.size), simulation)
        window.show()
        self.hide()
