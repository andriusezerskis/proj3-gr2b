from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton
from PyQt6.QtCore import Qt

from typing import Tuple, List
import sys


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random      # pour tester graphe, plus besoin apres
import matplotlib
matplotlib.use('QtAgg')

class MonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor deb'île")
        self.setGeometry(100, 100, 300, 200)

        # --- main layout settings ---
        self.layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # --- add widget on Vlayout ---
        title = QLabel('Tableau de bord-inator')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel{font-size: 20pt;}")
        self.layout.addWidget(title)

        # ---- second layout for selection ----
        # Hlayout containing 2 Vlayout (check button)
        #-> peut être le changer en stacked layout plus tard 
        # ou ajouter un truc QSpinBox à côté de rayon
        # 1 case = rayon de 1 enfaite 
        self.layout_2 = QHBoxLayout()
        self.check_zone = self.check_box()
        self.check_cata = self.check_box_2()

        self.layout_2.addWidget(self.check_zone)
        self.layout_2.addWidget(self.check_cata)

        self.container = QWidget()
        self.container.setLayout(self.layout_2)
        self.layout.addWidget(self.container)


        button = QPushButton("OK")
        button.clicked.connect(self.lol)
        self.layout.addWidget(button)
        


    def lol(self):
        # bouton OK handler
        print('lol')


    def check_box(self):
        layout = QVBoxLayout()

        label = QLabel("Choix de zone")
        layout.addWidget(label)

        b1 = QRadioButton("Case unique")
        b1.setChecked(True)
        b1.toggled.connect(lambda:self.btn_zone(b1))
        layout.addWidget(b1)

        b2 = QRadioButton("Rayon")
        b2.toggled.connect(lambda:self.btn_zone(b2))
        layout.addWidget(b2)

        b3 = QRadioButton("Ile")
        b3.toggled.connect(lambda:self.btn_zone(b3))
        layout.addWidget(b3)

        container = QWidget()
        container.setLayout(layout)
        return container

    def check_box_2(self):
        layout = QVBoxLayout()

        label = QLabel("Choix de catastrophe")
        layout.addWidget(label)

        b1 = QRadioButton("Froid glacial")
        b1.setChecked(True)
        b1.toggled.connect(lambda:self.btn_cata(b1))
        layout.addWidget(b1)

        b2 = QRadioButton("Super hot")
        b2.toggled.connect(lambda:self.btn_cata(b2))
        layout.addWidget(b2)

        b3 = QRadioButton("EXPLOSION")
        b3.toggled.connect(lambda:self.btn_cata(b3))
        layout.addWidget(b3)

        container = QWidget()
        container.setLayout(layout)
        return container

    def btn_zone(self,b):
        if b.text() == "Case unique":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
                
        if b.text() == "Rayon":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")

        if b.text() == "Ile":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")

    def btn_cata(self, b):
        if b.text() == "Froid glacial":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")
                
        if b.text() == "Super hot":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")

        if b.text() == "EXPLOSION":
            if b.isChecked() == True:
                print(b.text()+" is selected")
            else:
                print(b.text()+" is deselected")


        

app = QApplication(sys.argv)
w = MonitorWindow()
w.show()
app.exec()
