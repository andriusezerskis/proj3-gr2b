from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel
from model.entities.entity import Entity


class EntityInfoView(QDockWidget):
    def __init__(self, title: str, mainWindow: QWidget):
        super().__init__(title, mainWindow)
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.messageBox = QLabel()
        self.initialize()
        self.entity = None

    def initialize(self):
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.layout.addWidget(self.messageBox)
        self.messageBox.setText("No entities selected")
        
    def setEntity(self, entity: Entity):
        self.entity = entity

    def __updateText(self, entity: Entity):
        """Shows information about an entity"""
        self.entity = entity
        entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}"
        self.messageBox.setText(entity_info)
        if entity.isDead():
            self.showDeadEntity()

    def updateOnStep(self):
        if self.entity is not None:
            self.__updateText(self.entity)
        else:
            self.messageBox.setText("No entities selected")
            
    def showDeadEntity(self):
        self.messageBox.setText("Entity is dead")
