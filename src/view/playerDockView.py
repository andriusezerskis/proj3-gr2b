from PyQt6.QtWidgets import QDockWidget, QPushButton, QVBoxLayout

from src.constants import RELEASE_PLAYER
from src.model.entities.entity import Entity


class PlayerDockView(QDockWidget):
    def __init__(self, dock, container):
        super().__init__()
        self.dock = dock

        self.lageButton = QPushButton(RELEASE_PLAYER)
        self.lageButton.clicked.connect(self.lageEntity)
        #self.lageButton.hide()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lageButton)

        self.container = container
        self.container.setLayout(self.layout)

        self.entity = None

    def setEntity(self, entity: Entity):
        self.entity = entity

    def lageEntity(self):
        print("a")