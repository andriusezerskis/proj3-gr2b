

from constants import COMMANDS_WINDOW_TITLE, MOVE_CAMERA_UP
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget, QMainWindow


class CommandWindow(QMainWindow):
    def __init__(self, parent=None):
        super(CommandWindow, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.setWindowTitle(COMMANDS_WINDOW_TITLE)
        self.central_widget: QWidget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.createCommands()

    def createCommands(self):
        self.firstCommand = QLabel(MOVE_CAMERA_UP)
        self.layout.addWidget(self.firstCommand)
