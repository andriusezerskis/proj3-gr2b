"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,  QVBoxLayout, QLabel, QProgressBar, QPushButton
from controller.gridController import GridController
from model.entities.entity import Entity
from model.entities.animal import Animal
from controller.mainWindowController import MainWindowController

from parameters import ViewText, EntityParameters, ViewParameters


class EntityInfoView():
    def __init__(self,  container: QWidget):
        self.healthBar = QProgressBar()
        self.infoLabel = QLabel()

        self.hungerBar = QProgressBar()
        self.hungerBar.setRange(0, EntityParameters.MAX_HUNGER)
        self.hungerBar.hide()

        self.controlButton = QPushButton(ViewText.CONTROL_PLAYER)
        self.controlButton.clicked.connect(self.controlEntity)
        self.controlButton.setCheckable(True)
        self.controlButton.hide()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.healthBar)
        self.layout.addWidget(self.hungerBar)
        self.layout.addWidget(self.infoLabel)
        self.layout.addWidget(self.controlButton)
        self.layout.setAlignment(
            self.controlButton, Qt.AlignmentFlag.AlignCenter)

        self.container = container
        self.container.setLayout(self.layout)

        self.entity = None

    def controlEntity(self):
        GridController.getInstance().controlEntity(self.entity.getTile())
        # MainWindowController.getInstance().closeDock()
        MainWindowController.getInstance().changeDock()

    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity
        self.controlButton.show()

        self.healthBar.show()
        self.healthBar.setRange(0, entity.getMaxHealthPoints())
        self.healthBar.setValue(int(entity.getHealthPoints()))
        self.healthBar.setFormat(
            f"{ViewText.HEALTH_BAR_TEXT}{int(entity.getHealthPoints())}")

        baseText = f"{ViewText.NAME_TEXT}{entity.getName()}\n"
        baseText += f"{ViewText.AGE_TEXT}{entity.getDisplayAge()} jours\n"
        if isinstance(entity, Animal):
            self.hungerBar.show()
            preys = entity.getPreysNames()
            baseText += "Proie"
            if len(preys) > 1:
                baseText += f"s"
            baseText += ": "
            i = 0
            for prey in preys:
                baseText += f"{Entity.getFrenchNameFromClassName(prey)}"
                if i != len(preys) - 1:
                    baseText += ", "
                i += 1
            baseText += "\n"
            baseText += f"{entity.getCount()} {entity.getFrenchName().lower()}s\n"
            self.hungerBar.setFormat(f"{ViewText.HUNGER_TEXT}")
            self.hungerBar.setValue(int(entity.getHunger()))
        else:
            self.hungerBar.hide()
            baseText += f"{entity.getCount()} {entity.getFrenchName().lower()}s\n"
        self.infoLabel.setText(baseText)
        if entity.isDead():
            self.showDeadEntity()

    def updateOnStep(self):
        if self.entity is not None:
            self.__updateText(self.entity)
        else:
            self.hungerBar.setValue(0)
            self.hungerBar.setFormat(ViewText.ENTITY_NOT_SELECTED)
            self.healthBar.setValue(0)
            self.healthBar.setFormat(ViewText.ENTITY_NOT_SELECTED)

    def showDeadEntity(self):
        """
        When the entity dies, the progress bar shows that the entity is dead
        """
        self.hungerBar.setValue(0)
        self.hungerBar.setFormat(ViewText.ENTITY_DEAD_MESSAGE)
        self.healthBar.setValue(0)
        self.healthBar.setFormat(ViewText.ENTITY_DEAD_MESSAGE)
        self.infoLabel.clear()
        self.controlButton.hide()
        self.entity = None
