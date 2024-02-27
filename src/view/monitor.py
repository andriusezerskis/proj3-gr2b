"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QSpinBox, QComboBox, QButtonGroup
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import os


import matplotlib
from constants import CLICKED_BUTTON_STYLESHEET, NOT_CLICKED_BUTTON_STYLESHEET, Disaster
from model.entities.animals import Crab
from model.entities.entity import Entity

matplotlib.use('QtAgg')


class MonitorWindow:
    def __init__(self, dock, container):
        """
        Window for controlling catastrophe on the map >:)
        Display on the dock tab of main windows
        """
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
        self.infoZone = "Rayon"
        self.infoRayon = 10
        self.infoDisaster = "Froid glacial"
        self.isMonitor = False

        # Hlayout containing 2 Vlayout (check button)
        self.layout2 = QHBoxLayout()
        self.checkZone = self.checkBox()
        self.checkCata = self.checkBox2()

        self.layout2.addWidget(self.checkZone)
        self.layout2.addWidget(self.checkCata)

        self.container2 = QWidget()
        self.container2.setLayout(self.layout2)
        self.layout.addWidget(self.container2)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.okButtonCallback)
        self.button.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)
        self.layout.addWidget(self.button)

    def okButtonCallback(self):
        # handler of ok button after selection of a catastroph
        self.isMonitor = True
        self.button.setStyleSheet(CLICKED_BUTTON_STYLESHEET)

    def getIsMonitor(self):
        return self.isMonitor

    def offIsMonitor(self):
        # calls when click on the map after selection of catastroph
        # (end of the action)
        self.isMonitor = False
        self.button.setStyleSheet(NOT_CLICKED_BUTTON_STYLESHEET)

    def getInfo(self):
        return self.infoZone, self.infoRayon, self.infoDisaster, self.invasionChosen

    # ---- method for init GUI ----
    def checkBox(self):
        layout = QVBoxLayout()

        label = QLabel("Choix de zone")
        layout.addWidget(label)

        b2 = QRadioButton("Rayon")
        b2.setChecked(True)
        b2.toggled.connect(lambda: self.btnZone(b2))
        layout.addWidget(b2)

        spinBox = QSpinBox(minimum=1, maximum=100, value=10)
        spinBox.valueChanged.connect(self.updateSpinbox)
        layout.addWidget(spinBox)

        b3 = QRadioButton("Ile")
        b3.toggled.connect(lambda: self.btnZone(b3))
        layout.addWidget(b3)

        container = QWidget()
        container.setLayout(layout)
        return container

    def checkBox2(self):
        layout = QVBoxLayout()

        label = QLabel("Choix de catastrophe")
        layout.addWidget(label)

        b1 = QRadioButton(Disaster.ICE_TEXT, self.dock)
        b1.setChecked(True)
        b1.toggled.connect(lambda: self.btnCata(b1))
        layout.addWidget(b1)

        b2 = QRadioButton(Disaster.FIRE_TEXT, self.dock)
        b2.toggled.connect(lambda: self.btnCata(b2))
        layout.addWidget(b2)

        b3 = QRadioButton(Disaster.INVASION_TEXT, self.dock)
        b3.toggled.connect(lambda: self.btnCata(b3))

        combobox5 = QComboBox()

        for i in Entity.__subclasses__():
            for j in i.__subclasses__():
                animalIcon = QIcon(j.getDefaultTexturePath())
                combobox5.addItem(animalIcon, j.__name__)

        self.invasionChosen = combobox5.currentText()
        combobox5.currentTextChanged.connect(self.indexChanged)

        layout.addWidget(b3)
        layout.addWidget(combobox5)

        container = QWidget()
        container.setLayout(layout)
        return container

    def indexChanged(self, button):
        self.invasionChosen = button
        print(self.invasionChosen)

    # ---- handler for update information from button ----
    def btnZone(self, b):
        # handler de zone selectionné

        if b.isChecked() == True:
            self.infoZone = b.text()

    def updateSpinbox(self, value):
        self.infoRayon = value

    def btnCata(self, b):
        # handler de catastrophe selectionné

        if b.isChecked() == True:
            self.infoDisaster = b.text()


# --- for graph plot ---
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphWindow:
    def __init__(self, dock, container):
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
            print("hoho", i.__name__)
            for j in i.__subclasses__():
                print("haha", j.__name__)
                iconbutton = QPushButton(j.__name__)
                iconbutton.clicked.connect(
                    partial(self.setChosenEntity, j, iconbutton))
                icon = j.getDefaultTexturePath()
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
        self.setChosenEntity(j, iconbutton)

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
            plotRefs = self.canvas.axes.plot(
                self.xdata, self.ydata[self.chosenEntity], 'r')
            self._plotRef = plotRefs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plotRef.set_ydata(self.ydata[self.chosenEntity])
        self.drawPlot()
