"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QRadioButton, QSpinBox, QComboBox, QGroupBox
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import matplotlib
from utils import getTerminalSubclassesOfClass, getFrenchToEnglishTranslation
from model.disaster import Disaster
from parameters import ViewParameters
from model.entities.entity import Entity

matplotlib.use('QtAgg')


class MonitorWindow:
    def __init__(self,  container):
        """
        Window for controlling catastrophe on the map >:)
        Display on the dock tab of main windows
        """
        self.container = container
        self.layout = QVBoxLayout()

        self.container.setLayout(self.layout)

        # --- main layout settings ---
        title = QLabel('Tableau de bord-inator')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # tittle.setFont(QFont('Small Fonts', 20))
        title.setObjectName("title")
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

        self.button = QPushButton("Lancer la catastrophe")
        self.button.setCheckable(True)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, Qt.AlignmentFlag.AlignCenter)

    def getIsMonitor(self):
        return self.button.isChecked()

    def offIsMonitor(self):
        # calls when click on the map after selection of disaster
        self.button.setChecked(False)

    def getInfo(self):
        return self.infoZone, self.infoRayon, self.infoDisaster, self.invasionChosen

    # ---- method for init GUI ----
    def checkBox(self):
        layout = QVBoxLayout()

        rayonButton = QRadioButton("Rayon")
        rayonButton.setChecked(True)
        rayonButton.toggled.connect(lambda: self.btnZone(rayonButton))

        spinBox = QSpinBox(minimum=1, maximum=100, value=10)
        spinBox.valueChanged.connect(self.updateSpinbox)

        islandButton = QRadioButton("Ile")
        islandButton.toggled.connect(lambda: self.btnZone(islandButton))

        layout.addWidget(islandButton)
        layout.addWidget(rayonButton)
        layout.addWidget(spinBox)

        container = QGroupBox("Choix de la zone")
        container.setLayout(layout)
        return container

    def checkBox2(self):
        layout = QVBoxLayout()
        container = QGroupBox("Choix de catastrophe")
        container.setLayout(layout)

        iceButton = QRadioButton(Disaster.ICE_TEXT, self.container)
        iceButton.setChecked(True)
        iceButton.toggled.connect(lambda: self.btnCata(iceButton))
        layout.addWidget(iceButton)

        fireButton = QRadioButton(Disaster.FIRE_TEXT, self.container)
        fireButton.toggled.connect(lambda: self.btnCata(fireButton))
        layout.addWidget(fireButton)

        islandButton = QRadioButton(Disaster.INVASION_TEXT, self.container)
        islandButton.toggled.connect(lambda: self.btnCata(islandButton))

        combobox5 = QComboBox()

        for entityType in getTerminalSubclassesOfClass(Entity):
            assert issubclass(entityType, Entity)
            animalIcon = QIcon(entityType.getDefaultTexturePath())
            combobox5.addItem(animalIcon, entityType.getFrenchName())

        self.invasionChosen = getFrenchToEnglishTranslation(
            combobox5.currentText())
        combobox5.currentTextChanged.connect(self.indexChanged)

        layout.addWidget(islandButton)
        layout.addWidget(combobox5)

        return container

    def indexChanged(self, button: str):
        self.invasionChosen = getFrenchToEnglishTranslation(button)

    # ---- handler for update information from button ----
    def btnZone(self, zoneButton):
        if zoneButton.isChecked() == True:
            self.infoZone = zoneButton.text()

    def updateSpinbox(self, value):
        self.infoRayon = value

    def btnCata(self, disasterButton):
        if disasterButton.isChecked() == True:
            self.infoDisaster = disasterButton.text()


# --- for graph plot ---
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor(eval(ViewParameters.FIG_BCKGROUND))
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphWindow:
    def __init__(self,  container):
        # --- graph ----
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout = QVBoxLayout()
        container.setLayout(self.layout)
        self.layout.addWidget(self.canvas)

        # --- buttons range with different entities ---
        iconWidget = QWidget()
        iconLayout = QVBoxLayout()
        iconsubLayout = QHBoxLayout()
        iconsubLayout2 = QHBoxLayout()
        iconsubWidget = QWidget()
        iconsubWidget2 = QWidget()
        iconsubWidget.setLayout(iconsubLayout)
        iconsubWidget2.setLayout(iconsubLayout2)
        iconLayout.addWidget(iconsubWidget)
        iconLayout.addWidget(iconsubWidget2)
        self.chosenEntity = []

        iconWidget.setLayout(iconLayout)
        self.layout.addWidget(iconWidget)
        self.iconButtonSelected = None
        # range display
        nData = 50
        self.xdata = list(range(nData))
        self.nData = nData
        self.ydata = {}

        for entityType in getTerminalSubclassesOfClass(Entity):
            self.ydata[entityType] = [0 for k in range(nData)]

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plotRef = None

        for index, entityType in enumerate(getTerminalSubclassesOfClass(Entity)):
            assert issubclass(entityType, Entity)
            # text = Text(entityType.getFrenchName())
            iconbutton = QPushButton(entityType.getFrenchName())
            iconbutton.setCheckable(True)
            self.setChosenEntity(entityType, iconbutton)
            iconbutton.clicked.connect(
                partial(self.setChosenEntity, entityType, iconbutton))
            icon = entityType.getDefaultTexturePath()
            iconbutton.setStyleSheet(
                "QPushButton:checked {background-color: rgba(159, 134, 109, 1); color: rgba(247, 229, 209, 1); border-radius: 3px;} QPushButton {background-color: " + entityType.getColor()+"; color: white ; border-radius: 3px;}")
            iconbutton.setIcon(
                QIcon(icon))
            iconbutton.setIconSize(QSize(15, 15))
            if len(getTerminalSubclassesOfClass(Entity)) / 2 > index:
                iconsubLayout.addWidget(iconbutton)
            else:
                iconsubLayout2.addWidget(iconbutton)

    def setChosenEntity(self, entity, iconbutton):
        if iconbutton.isChecked():

            self.chosenEntity.remove(entity)

        else:

            self.chosenEntity.append(entity)
        self.drawPlot()

    def drawPlot(self):
        self.canvas.axes.clear()
        ylim = 0
        for entity in self.chosenEntity:
            self.canvas.axes.plot(self.xdata, self.ydata[entity], color=entity.getColor(
            ), label=entity.getFrenchName())
            if max(self.ydata[entity]) * 1.15 > ylim:
                ylim = 1.15 * max(self.ydata[entity])

        self.canvas.axes.set_ylim(0, ylim)
        """
        if self.chosenEntity.getFrenchName()[0] in "AEIOUYH":
            self.canvas.axes.set_title(
                f"Évolution de la population d' " + self.chosenEntity.getFrenchName().lower() + "s")
        else:
            self.canvas.axes.set_title(
                f"Évolution de la population de " + self.chosenEntity.getFrenchName().lower() + "s")"""

        title = "Évolution des populations" if len(
            self.chosenEntity) != 1 else "Évolution de la population "

        self.canvas.axes.set_title(title if len(
            self.chosenEntity) > 0 else "Veuillez sélectionner\n une entitée")
        self.canvas.axes.set_facecolor(eval(ViewParameters.PLOT_BCKGROUND))
        self.canvas.axes.set_ylabel("Quantité")
        self.canvas.draw()

    def updatePlot(self, newNumber, entity):
        self.ydata[entity] = self.ydata[entity][1:] + [newNumber]

        self.drawPlot()
