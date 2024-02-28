"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtWidgets import QDockWidget,  QVBoxLayout, QLabel, QProgressBar, QPushButton, QHBoxLayout
from controller.gridController import GridController
from model.entities.entity import Entity
from model.entities.animal import Animal
from constants import CONTROL_PLAYER, ENTITY_DEAD_MESSAGE, ENTITY_MAX_HUNGER, ENTITY_NOT_SELECTED, ENTITY_PARAMETERS, RELEASE_PLAYER
from view.cssConstants import PROGRESS_BAR


class EntityInfoView(QDockWidget):
    def __init__(self, dock, container):
        super().__init__()
        self.dock = dock

        self.healthBar = QProgressBar()
        self.healthBar.setStyleSheet(PROGRESS_BAR)
        self.infoLabel = QLabel()

        self.hungerBar = QProgressBar()
        self.hungerBar.setRange(0, ENTITY_MAX_HUNGER)
        self.hungerBar.setStyleSheet(PROGRESS_BAR)
        self.hungerBar.hide()

        self.controlButton = QPushButton(CONTROL_PLAYER)
        self.controlButton.clicked.connect(self.controlEntity)
        self.controlButton.hide()

        self.lageButton = QPushButton(RELEASE_PLAYER)
        self.lageButton.clicked.connect(self.controlEntity)
        self.lageButton.hide()

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.controlButton)
        self.buttonLayout.addWidget(self.lageButton)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.healthBar)
        self.layout.addWidget(self.hungerBar)
        self.layout.addWidget(self.infoLabel)
        self.layout.addLayout(self.buttonLayout)

        self.container = container
        self.container.setLayout(self.layout)

        self.entity = None

    def controlEntity(self):
        GridController.getInstance().controlEntity(self.entity.getTile())

    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity
        self.controlButton.show()
        self.lageButton.show()

        self.healthBar.show()
        self.healthBar.setValue(int(entity.getHealthPoints()))
        self.healthBar.setRange(0, entity.getMaxHealthPoints())
        self.healthBar.setFormat("Santé")

        baseText = f"Prénom: {entity.getName()}\n"
        baseText += f"Âge: {entity.getDisplayAge()} jours\n"
        if isinstance(entity, Animal):
            self.hungerBar.show()
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
            self.hungerBar.setFormat("Faim")
            self.hungerBar.setValue(int(entity.getHunger()))
        else:
            self.hungerBar.hide()
            baseText += f"{entity.getCount()} {ENTITY_PARAMETERS[entity.__class__.__name__]['french_name'].lower()}s\n"
        self.infoLabel.setText(baseText)
        if entity.isDead():
            self.showDeadEntity()

    def updateOnStep(self):
        if self.entity is not None:
            self.__updateText(self.entity)
        else:
            self.hungerBar.setValue(0)
            self.hungerBar.setFormat(ENTITY_NOT_SELECTED)
            self.healthBar.setValue(0)
            self.healthBar.setFormat(ENTITY_NOT_SELECTED)

    def showDeadEntity(self):
        """
        When the entity dies, the progress bar shows that the entity is dead
        """
        self.hungerBar.setValue(0)
        self.hungerBar.setFormat(ENTITY_DEAD_MESSAGE)
        self.healthBar.setValue(0)
        self.healthBar.setFormat(ENTITY_DEAD_MESSAGE)
        self.infoLabel.clear()
        self.entity = None
