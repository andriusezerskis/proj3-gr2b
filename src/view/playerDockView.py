from PyQt6.QtWidgets import QDockWidget, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout,  QTextEdit
from PyQt6.QtGui import QPixmap, QIcon

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
        # self.lageButton.hide()

        self.peche = QPushButton("Débloquer")
        self.peche.setFixedSize(200, 40)
        self.peche.setIcon(
            QIcon(QPixmap("../assets/textures/items/fishing_rod.png")))
        # self.lageButton.hide()

        self.woodIcon = QTextEdit()
        self.woodIcon.setReadOnly(True)
        self.woodIcon.setFixedSize(200, 40)
        self.woodIcon.setHtml(
            """
<table width="100%">
    <tr>
        <td><img src='../assets/textures/items/wood.png' width='25' height='25'></td>
        <td style="vertical-align: middle;"> 5 </td>
        <td><img src='../assets/textures/items/claw.png' width='25' height='25'></td>
        <td style="vertical-align: middle;"> 3 </td>
    </tr>
</table>
""")

        self.secondLayout = QHBoxLayout()
        self.secondLayout.addWidget(self.peche)
        self.secondLayout.addWidget(self.woodIcon)

        self.secondContainer = QWidget()
        self.secondContainer.setLayout(self.secondLayout)

        self.firstLayout = QVBoxLayout()
        self.firstLayout.addWidget(self.freeButton)
        self.firstLayout.addWidget(self.secondContainer)

        self.container = container
        self.container.setLayout(self.firstLayout)

        self.entity = None

    def setEntity(self, entity: Entity):
        self.entity = entity

    def lageEntity(self):
        GridController.getInstance().lageEntity()
        MainWindowController.getInstance().changeDock()
