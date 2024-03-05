from PyQt6.QtWidgets import QDockWidget, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout,  QTextEdit
from PyQt6.QtGui import QPixmap, QIcon

from constants import RELEASE_PLAYER
from controller.mainWindowController import MainWindowController
from model.entities.entity import Entity
from controller.gridController import GridController

from model.crafting.crafts import FishingRod
from model.crafting.loots import *


class PlayerDockView(QDockWidget):
    def __init__(self, dock, container):
        super().__init__()
        self.dock = dock

        self.freeButton = QPushButton(RELEASE_PLAYER)
        self.freeButton.clicked.connect(self.lageEntity)
        # self.lageButton.hide()

        self.peche = QPushButton("Débloquer")
        self.peche.setFixedSize(200, 40)
        self.peche.clicked.connect(self.unlockFishing)
        self.peche.setIcon(QIcon(QPixmap(FishingRod.getDefaultTexturePath())))
        # self.lageButton.hide()

        self.woodIcon = QTextEdit()
        self.woodIcon.setReadOnly(True)
        self.woodIcon.setFixedSize(200, 40)
        self.woodIcon.setHtml(self.createHTML(FishingRod))

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

    def unlockFishing(self):
        if MainWindowController.getInstance().unlockFishing():
            self.peche.setText("Canne à pêche débloquée")

    @staticmethod
    def createHTML(craftable_item):
        res = """<table width="100%"><tr>"""
        blueprint = craftable_item.getBlueprint()
        for item, quantity in blueprint.items():
            item_class = eval(item)
            texture = item_class.getDefaultTexturePath()

            res += f"""<td><img src='{texture}' width='25' height='25'></td>
                <td style="vertical-align: middle;"> {quantity} </td>"""
        res += """</tr></table>"""
        return res
