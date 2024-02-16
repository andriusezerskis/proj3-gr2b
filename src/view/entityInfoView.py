from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel, QProgressBar
from model.entities.entity import Entity
from model.entities.animal import Animal
from model.entities.plant import Plant
from constants import ENTITY_MAX_HUNGER, ENTITIES_NAMES_TRANSLATION
from PyQt6.QtWidgets import QHBoxLayout


class EntityInfoView(QDockWidget):
    def __init__(self, dock, container):
        self.dock = dock
        self.container = container
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)
        self.progressBar = QProgressBar()
        self.infoLabel = QLabel()
        self.initialize()
        self.entity = None

    def initialize(self):
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.infoLabel)

        self.progressBar.setRange(0, ENTITY_MAX_HUNGER)

    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity
        baseText = f"Âge: {entity.getAge()}\n"
        if isinstance(entity, Animal):
            self.progressBar.show()
            preys = entity.getPreys()
            baseText += f"Proie(s): "
            i = 0
            for prey in preys:
                baseText += f"{ENTITIES_NAMES_TRANSLATION[prey.__name__]}"
                if i != len(preys) - 1:
                    baseText += ", "
                i += 1
            baseText += "\n"
            baseText += f"{entity.count} {ENTITIES_NAMES_TRANSLATION[entity.__class__.__name__].lower()}s\n"
            self.progressBar.setFormat("Faim")
            self.progressBar.setValue(entity.getHunger())
        else:
            self.progressBar.hide()
            baseText += f"{entity.count} {ENTITIES_NAMES_TRANSLATION[entity.__class__.__name__].lower()}s\n"
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
