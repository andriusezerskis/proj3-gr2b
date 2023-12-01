from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget

from typing import Tuple, List
import sys

class MonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor deb'île")
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout()

        # self.label = QLabel("WIL THE BEST MUUUWWZIKK")
        # self.layout.addWidget(self.label)

        # button = QPushButton("DJ KHALEDDDD")
        # button.clicked.connect(self.lol)
        # self.layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.slot_1 = self.slot("Choisir une coordonnée", "0, 0")
        self.slot_2 = self.slot("Température de la zone", "0°")

        self.layout.addWidget(self.slot_1)
        self.layout.addWidget(self.slot_2)

        label_2 = QLabel('yo')
        self.layout.addWidget(label_2)



    def lol(self):
    	print('lol')

    def slot(self, button, text):
        slot_1 = QHBoxLayout()
        button = QPushButton(button)
        button.clicked.connect(self.lol)
        slot_1.addWidget(button)

        label = QLabel(text)
        slot_1.addWidget(label)        

        container = QWidget()
        container.setLayout(slot_1)
        return container

app = QApplication(sys.argv)
w = MonitorWindow()
w.show()
app.exec()