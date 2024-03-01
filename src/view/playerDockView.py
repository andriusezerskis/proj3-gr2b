from PyQt6.QtWidgets import QDockWidget, QPushButton, QVBoxLayout

from constants import RELEASE_PLAYER
from controller.mainWindowController import MainWindowController
from model.entities.entity import Entity
from controller.gridController import GridController


class PlayerDockView(QDockWidget):
    def __init__(self, dock, container):
        super().__init__()
        self.dock = dock

        self.freeButton = QPushButton(RELEASE_PLAYER)
        self.freeButton.clicked.connect(self.lageEntity)
        #self.lageButton.hide()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.freeButton)

        self.container = container
        self.container.setLayout(self.layout)

        self.entity = None

    def setEntity(self, entity: Entity):
        self.entity = entity

    def lageEntity(self):
        GridController.getInstance().lageEntity()
        MainWindowController.getInstance().changeDock()