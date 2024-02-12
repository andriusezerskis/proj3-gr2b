from PyQt6.QtWidgets import QMessageBox, QDockWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon


class EntityInfoView(QDockWidget):
    def __init__(self, title: str, mainWindow):
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

    def updateOnClick(self, entity):
        """Shows information about an entity"""
        self.entity = entity
        entity_info = f"Age: {entity.getAge()}\nHunger: {entity.getHunger()}"
        self.messageBox.setText(entity_info)

    def updateOnStep(self):
        if self.entity:
            self.updateOnClick(self.entity)
        else:
            self.messageBox.setText("No entities selected")
