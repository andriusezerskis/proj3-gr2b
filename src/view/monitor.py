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

        self.slot__1_widget = self.slot1()

        self.layout.addWidget(self.slot__1_widget)

        label_2 = QLabel('yo')
        self.layout.addWidget(label_2)



    def lol(self):
    	print('lol')

    def slot1(self):
        slot_1 = QHBoxLayout()
        button = QPushButton("DJ KHALEDDDD")
        button.clicked.connect(self.lol)
        slot_1.addWidget(button)

        label = QLabel("WIL THE BEST MUUUWWZIKK")
        slot_1.addWidget(label)        

        container = QWidget()
        container.setLayout(slot_1)
        return container

app = QApplication(sys.argv)
w = MonitorWindow()
w.show()
app.exec()