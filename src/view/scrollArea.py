"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from typing import Dict, List

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QGroupBox

from model.crafting.loots import Loot
from utils import getTerminalSubclassesOfClass


class ScrollArea(QWidget):
    def __init__(self, container: QWidget):
        super().__init__()
        self.scrollArea = QScrollArea()
        self.quantities: Dict[str: List[QLabel, QLabel]] = {}
        self.initUI(container)

    def initUI(self, container: QWidget):
        layout = QVBoxLayout()
        contentWidget = QGroupBox("Inventaire")
        self.scrollArea.setWidget(contentWidget)
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setHorizontalScrollBarPolicy(False)  # ScrollBarAlwaysOff

        scrollLayout = QVBoxLayout()
        contentWidget.setLayout(scrollLayout)

        # Ajoutez des images à la liste
        for itemsClass in getTerminalSubclassesOfClass(Loot):
            h_layout = QHBoxLayout()
            pixmap = QPixmap(itemsClass.getDefaultTexturePath())
            # pixmap.scaled(2048, 2048)
            image = QLabel()
            image.resize(200, 200)
            image.setPixmap(pixmap)
            h_layout.addWidget(image)
            text = QLabel()
            text.setText("0")
            self.quantities[itemsClass.__name__] = [image, text]
            h_layout.addWidget(text)
            scrollLayout.addLayout(h_layout)

        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        container.setLayout(layout)

    def update_content(self, loots):
        for items in loots:
            self.quantities[items][1].setText(str(loots[items]))
