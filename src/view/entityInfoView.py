from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel, QProgressBar
from model.entities.entity import Entity
from constants import ENTITY_MAX_HUNGER


class EntityInfoView(QDockWidget):
    def __init__(self, title: str, mainWindow: QWidget):
        super().__init__(title, mainWindow)
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.progressBar = QProgressBar()
        self.initialize()
        self.entity = None

    def initialize(self):
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.layout.addWidget(self.progressBar)
        self.progressBar.setRange(0, ENTITY_MAX_HUNGER)
        
    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity
        """entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}"
        self.messageBox.setText(entity_info)"""
        self.progressBar.setValue(entity.getHunger())
        if entity.isDead():
            self.showDeadEntity()

    def updateOnStep(self):
        if self.entity is not None:
            self.__updateText(self.entity)
        else:
            self.progressBar.setValue(0)
            self.progressBar.setFormat("No entities selected")
            #self.messageBox.setText("No entities selected")
            
    def showDeadEntity(self):
        self.progressBar.setValue(0)
        self.progressBar.setFormat("Entity is dead")
