from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDockWidget,  QVBoxLayout, QLabel, QProgressBar, QPushButton, QHBoxLayout
from controller.gridController import GridController
from model.entities.entity import Entity
from model.entities.animal import Animal
from constants import ENTITY_MAX_HUNGER, ENTITY_PARAMETERS
from PyQt6.QtWidgets import QHBoxLayout

from controller.mainWindowController import MainWindowController


class EntityInfoView(QDockWidget):
    def __init__(self, dock, container):
        super().__init__()
        self.dock = dock
        self.container = container
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)
        self.progressBar = QProgressBar()
        self.infoLabel = QLabel()
        self.buttonLayout = QHBoxLayout()
        self.controlButton = QPushButton("Contrôler")
        self.lageButton = QPushButton("Relâcher")
        self.initialize()
        self.entity = None

    def initialize(self):
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.infoLabel)
        self.controlButton.clicked.connect(self.controlEntity)
        self.lageButton.clicked.connect(self.controlEntity)
        self.controlButton.hide()
        self.lageButton.hide()
        self.buttonLayout.addWidget(self.controlButton)
        self.buttonLayout.addWidget(self.lageButton)
        self.buttonLayout.setParent(None)
        self.layout.addLayout(self.buttonLayout)
        self.layout.setAlignment(
            self.buttonLayout, Qt.AlignmentFlag.AlignBottom)

        self.progressBar.setRange(0, ENTITY_MAX_HUNGER)
        self.progressBar.hide()

    def controlEntity(self):
        GridController.getInstance().controlEntity(self.entity.getTile())

    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity
        self.controlButton.show()
        self.lageButton.show()
        baseText = f"Âge: {entity.getDisplayAge()} jours\n"
        if isinstance(entity, Animal):
            self.progressBar.show()
            preys = entity.getPreysNames()
            baseText += "Proie"
            if len(preys) > 1:
                baseText += f"s"
            baseText += ": "
            i = 0
            for prey in preys:
                baseText += f"{ENTITY_PARAMETERS[prey]['french_name']}"
                if i != len(preys) - 1:
                    baseText += ", "
                i += 1
            baseText += "\n"
            baseText += f"{entity.getCount()} {ENTITY_PARAMETERS[entity.__class__.__name__]['french_name'].lower()}s\n"
            self.progressBar.setFormat("Faim")
            self.progressBar.setValue(int(entity.getHunger()))
        else:
            self.progressBar.hide()
            baseText += f"{entity.getCount()} {ENTITY_PARAMETERS[entity.__class__.__name__]['french_name'].lower()}s\n"
        self.infoLabel.setText(baseText)
        print(entity.getPos())
        if entity.isDead():
            self.showDeadEntity()

    def updateOnStep(self):
        if self.entity is not None:
            self.__updateText(self.entity)
        else:
            self.progressBar.setValue(0)
            self.progressBar.setFormat("Pas d'entité sélectionnée")

    def showDeadEntity(self):
        self.progressBar.setValue(0)
        self.progressBar.setFormat("L'entité est morte")
        self.entity = None
