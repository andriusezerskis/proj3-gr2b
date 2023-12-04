from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from typing import Tuple, List
import sys

class MonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor deb'île")
        self.setGeometry(100, 100, 200, 300)
        self.layout = QVBoxLayout()

        # self.label = QLabel("WIL THE BEST MUUUWWZIKK")
        # self.layout.addWidget(self.label)

        # button = QPushButton("DJ KHALEDDDD")
        # button.clicked.connect(self.lol)
        # self.layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.slot_1 = self.slot_choose_coord()
        self.slot_2 = self.slot_temperature()

        self.layout.addWidget(self.slot_1)
        self.layout.addWidget(self.slot_2)

        label_2 = QLabel('yo')
        self.layout.addWidget(label_2)

#faire une classe slot comme ça pour manipuler les label etc c carré

    def lol(self):
    	print('lol')

    def slot_choose_coord(self):
        slot = QHBoxLayout()
        button = QPushButton("Choisir une coordonnée")
        button.clicked.connect(self.lol)
        slot.addWidget(button)

        label = QLabel("0, 0")
        slot.addWidget(label)        

        container = QWidget()
        container.setLayout(slot)
        return container

    def slot_temperature(self):
        slot = QHBoxLayout()
        label = QLabel("Température de la région")
        slot.addWidget(label)
        label = QLabel("t°")
        slot.addWidget(label)

        container = QWidget()
        container.setLayout(slot)
        return container

app = QApplication(sys.argv)
w = MonitorWindow()
w.show()
app.exec()