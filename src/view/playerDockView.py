from PyQt6.QtWidgets import QDockWidget, QPushButton, QVBoxLayout, QWidget

from parameters import ViewText
from controller.mainWindowController import MainWindowController
from controller.gridController import GridController


class PlayerDockView(QDockWidget):
    def __init__(self,  container: QWidget):
        super().__init__()

        self.lageButton = QPushButton(ViewText.RELEASE_PLAYER)
        self.lageButton.clicked.connect(self.lageEntity)
        # self.lageButton.hide()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lageButton)

        self.container = container
        self.container.setLayout(self.layout)

    @staticmethod
    def lageEntity():
        GridController.getInstance().lageEntity()
        MainWindowController.getInstance().changeDock()
