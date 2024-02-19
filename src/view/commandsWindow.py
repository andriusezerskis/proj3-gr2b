"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from constants import COMMANDS_WINDOW_TITLE, MOVE_CAMERA_UP
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget, QMainWindow


class CommandWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CommandWindow, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.setWindowTitle(COMMANDS_WINDOW_TITLE)
        self.centralWidget: QWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.drawCommands()

    def drawCommands(self):
        """
        Draw the commands that the user can use to move the player
        """
        self.firstCommand = QLabel(MOVE_CAMERA_UP)
        self.layout.addWidget(self.firstCommand)
