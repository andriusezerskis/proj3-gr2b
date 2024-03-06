"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from model.crafting.loots import Loot


class ScrollArea(QWidget):
    def __init__(self, container: QWidget):
        super().__init__()
        self.scrollArea = QScrollArea()
        self.initUI(container)

    def initUI(self, container: QWidget):
        layout = QVBoxLayout()
        contentWidget = QWidget()
        self.scrollArea.setWidget(contentWidget)
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setHorizontalScrollBarPolicy(False)  # ScrollBarAlwaysOff

        scrollLayout = QVBoxLayout()
        contentWidget.setLayout(scrollLayout)

        # Ajoutez des images à la liste
        for itemsClass in Loot.__subclasses__():
            pixmap = QPixmap(itemsClass.getDefaultTexturePath())
            pixmap = pixmap.scaled(32, 32)
            label = QLabel()
            label.setPixmap(pixmap)
            scrollLayout.addWidget(label)

        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        container.setLayout(layout)
