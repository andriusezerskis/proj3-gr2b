from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton
from PyQt6.QtCore import Qt

from typing import Tuple, List
import sys

class MonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor deb'île")
        self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()

        # self.label = QLabel("WIL THE BEST MUUUWWZIKK")
        # self.layout.addWidget(self.label)

        # button = QPushButton("DJ KHALEDDDD")
        # button.clicked.connect(self.lol)
        # self.layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.label_2 = QLabel('Tableau de bord-inator')
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_2.setStyleSheet("QLabel{font-size: 20pt;}")

        self.layout.addWidget(self.label_2)

        #self.slot_1 = self.slot_choose_coord()
        #self.slot_2 = self.slot_temperature()
        self.layout_2 = QHBoxLayout()
        self.check_zone = self.check_box()
        self.check_cata = self.check_box_2()

        self.layout_2.addWidget(self.check_zone)
        self.layout_2.addWidget(self.check_cata)

        self.container = QWidget()
        self.container.setLayout(self.layout_2)


        #self.layout.addWidget(self.slot_1)
        #self.layout.addWidget(self.slot_2)
        self.layout.addWidget(self.container)

        button = QPushButton("OK")
        button.clicked.connect(self.lol)
        self.layout.addWidget(button)

        

# faire une classe slot comme ça pour manipuler les label etc c carré

    def lol(self):
        print('lol')

    def slot_choose_coord(self):
        slot = QHBoxLayout()
        button = QPushButton("Choisir une coordonnée")
        button.clicked.connect(self.lol)

        # my_font = QFont("Times New Roman", 12)
        # my_button.setFont(my_font)
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


    def check_box(self):
        layout = QVBoxLayout()

        label = QLabel("Choix de zone")
        layout.addWidget(label)

        self.b1 = QRadioButton("Button1")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)

        self.b2 = QRadioButton("Button2")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        layout.addWidget(self.b2)

        self.b3 = QRadioButton("Button3")
        #self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        layout.addWidget(self.b3)

        container = QWidget()
        container.setLayout(layout)
        return container

    def check_box_2(self):
        layout = QVBoxLayout()

        label = QLabel("Choix de catastrophe")
        layout.addWidget(label)

        self.b1 = QRadioButton("Button1")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        layout.addWidget(self.b1)

        self.b2 = QRadioButton("Button2")
        self.b2.toggled.connect(lambda:self.btnstate(self.b2))
        layout.addWidget(self.b2)

        self.b3 = QRadioButton("Button3")
        #self.b3.toggled.connect(lambda:self.btnstate(self.b3))
        layout.addWidget(self.b3)

        container = QWidget()
        container.setLayout(layout)
        return container

    def btnstate(self,b):
    
      if b.text() == "Button1":
         if b.isChecked() == True:
            print(b.text()+" is selected")
         else:
            print(b.text()+" is deselected")
                
      if b.text() == "Button2":
         if b.isChecked() == True:
            print(b.text()+" is selected")
         else:
            print(b.text()+" is deselected")
        

app = QApplication(sys.argv)
w = MonitorWindow()
w.show()
app.exec()
