"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QSpinBox
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import os


import matplotlib
from constants import CLICKED_BUTTON_STYLESHEET, NOT_CLICKED_BUTTON_STYLESHEET
from model.entities.animals import Crab
from model.entities.entity import Entity

matplotlib.use('QtAgg')


class MonitorWindow:
    def __init__(self, dock, container):
        self.rayon = 20
        self.dock = dock
        self.container = container
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)

        # --- main layout settings ---
        title = QLabel('Tableau de bord-inator')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel{font-size: 20pt;}")
        self.layout.addWidget(title)

        # ---- second layout for selection ----
        # Hlayout containing 2 Vlayout (check button)
        # -> peut être le changer en stacked layout plus tard
        # ou ajouter un truc QSpinBox à côté de rayon
        # 1 case = rayon de 1 enfaite
        self.layout2 = QHBoxLayout()
        self.checkZone = self.check_box()
        self.checkCata = self.check_box_2()

        self.layout2.addWidget(self.checkZone)
        self.layout2.addWidget(self.checkCata)

        self.container2 = QWidget()
        self.container2.setLayout(self.layout2)
        self.layout.addWidget(self.container2)

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

        # b1 = QRadioButton("Case unique")
        # b1.setChecked(True)
        # b1.toggled.connect(lambda:self.btn_zone(b1))
        # layout.addWidget(b1)

        b2 = QRadioButton("Rayon")
        b2.setChecked(True)
        b2.toggled.connect(lambda: self.btn_zone(b2))
        layout.addWidget(b2)

        spin_box = QSpinBox(minimum=1, maximum=100, value=20)
        spin_box.valueChanged.connect(self.updateSpinbox)
        layout.addWidget(spin_box)

        b3 = QRadioButton("Ile")
        b3.toggled.connect(lambda: self.btn_zone(b3))
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
        b1.toggled.connect(lambda: self.btnCata(b1))
        layout.addWidget(b1)

        b2 = QRadioButton("Super hot")
        b2.toggled.connect(lambda: self.btnCata(b2))
        layout.addWidget(b2)

        b3 = QRadioButton("EXPLOSION")
        b3.toggled.connect(lambda: self.btnCata(b3))
        layout.addWidget(b3)

        container = QWidget()
        container.setLayout(layout)
        return container

    def btn_zone(self, b):
        # handler de zone selectionné
        # if b.text() == "Case unique":
        #     if b.isChecked() == True:
        #         print(b.text()+" is selected")
        #     else:
        #         print(b.text()+" is deselected")

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

    def updateSpinbox(self, value):
        self.rayon = value

    def btnCata(self, b):
        # handler de catastrophe selectionné
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


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphWindow:
    def __init__(self, dock, container):
        # self.setGeometry(500, 100, 500, 300)

        # --- graph ----
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout = QVBoxLayout()
        container.setLayout(self.layout)
        self.layout.addWidget(self.canvas)
        iconWidget = QWidget()
        iconLayout = QHBoxLayout()
        iconWidget.setLayout(iconLayout)
        self.layout.addWidget(iconWidget)
        self.iconButtonSelected = None

        for i in Entity.__subclasses__():
            for j in i.__subclasses__():
                iconbutton = QPushButton(j.__name__)
                iconbutton.clicked.connect(
                    partial(self.setChosenEntity, j, iconbutton))
                icon = j.getTexturePath()
                iconbutton.setIcon(
                    QIcon(icon))
                iconbutton.setIconSize(QSize(15, 15))
                iconbutton.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)

                iconLayout.addWidget(iconbutton)

        nData = 50
        self.xdata = list(range(nData))
        self.nData = nData
        self.ydata = {}

        for i in Entity.__subclasses__():
            for j in i.__subclasses__():
                self.ydata[j] = [0 for k in range(nData)]

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plotRef = None
        self.chosenEntity = Crab

    def setChosenEntity(self, entity, iconbutton):
        if iconbutton.styleSheet() == NOT_CLICKED_BUTTON_STYLESHEET:  # not chosen
            iconbutton.setStyleSheet(CLICKED_BUTTON_STYLESHEET)  # chosen
            if self.iconButtonSelected:
                self.iconButtonSelected.setStyleSheet(
                    NOT_CLICKED_BUTTON_STYLESHEET)
            self.iconButtonSelected = iconbutton
        else:
            iconbutton.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)
        self.chosenEntity = entity
        print("changed", self.chosenEntity.__name__)
        self.drawPlot()

    def drawPlot(self):
        self.canvas.axes.clear()
        self.canvas.axes.plot(self.xdata, self.ydata[self.chosenEntity], 'r')
        self.canvas.axes.set_ylim(
            0, max(max(self.ydata[self.chosenEntity]), 1))
        self.canvas.draw()

    def updatePlot(self, newNumber, entity):
        self.ydata[entity] = self.ydata[entity][1:] + [newNumber]

        # Note: we no longer need to clear the axis.
        if self._plotRef is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(
                self.xdata, self.ydata[self.chosenEntity], 'r')
            self._plotRef = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plotRef.set_ydata(self.ydata[self.chosenEntity])
        self.drawPlot()
