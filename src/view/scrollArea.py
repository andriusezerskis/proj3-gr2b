from typing import Dict, List

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout

from model.crafting.loots import Loot
from utils import getTerminalSubclassesOfClass


class ScrollArea(QWidget):
    def __init__(self, container):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.quantities: Dict[str: List[QLabel, QLabel]] = {}
        self.initUI(container)

    def initUI(self, container):
        layout = QVBoxLayout()
        content_widget = QWidget()
        self.scroll_area.setWidget(content_widget)
        self.scroll_area.setWidgetResizable(True)
        #self.scroll_area.setHorizontalScrollBarPolicy(False)  # ScrollBarAlwaysOff

        scroll_layout = QVBoxLayout()
        content_widget.setLayout(scroll_layout)

        # Ajoutez des images à la liste
        for items_class in getTerminalSubclassesOfClass(Loot):
            h_layout = QHBoxLayout()
            pixmap = QPixmap(items_class.getDefaultTexturePath())
            #pixmap.scaled(2048, 2048)
            image = QLabel()
            image.resize(200, 200)
            image.setPixmap(pixmap)
            h_layout.addWidget(image)
            text = QLabel()
            text.setText("0")
            self.quantities[items_class.__name__] = [image, text]
            h_layout.addWidget(text)
            scroll_layout.addLayout(h_layout)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)
        container.setLayout(layout)

    def update_content(self, loots):
        for items in loots:
            self.quantities[items][1].setText(str(loots[items]))
        #print(self.quantities)

