from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from model.crafting.loots import Loot


class ScrollArea(QWidget):
    def __init__(self, container):
        super().__init__()
        self.scrollArea = QScrollArea()
        self.initUI(container)

    def initUI(self, container):
        layout = QVBoxLayout()
        contentWidget = QWidget()
        self.scrollArea.setWidget(contentWidget)
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setHorizontalScrollBarPolicy(False)  # ScrollBarAlwaysOff

        scrollLayout = QVBoxLayout()
        contentWidget.setLayout(scrollLayout)

        # Ajoutez des images à la liste
        for itemsClass in Loot.__subclasses__():
            for _ in range(100):
                print(itemsClass.getDefaultTexturePath())
                pixmap = QPixmap(itemsClass.getDefaultTexturePath())
                pixmap.scaled(2048, 2048)
                label = QLabel()
                label.setPixmap(pixmap)
                scrollLayout.addWidget(label)

        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        container.setLayout(layout)
