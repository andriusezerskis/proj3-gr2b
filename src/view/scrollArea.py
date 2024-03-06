from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from model.crafting.loots import Loot


class ScrollArea(QWidget):
    def __init__(self, container):
        super().__init__()
        self.scroll_area = QScrollArea()
        self.initUI(container)

    def initUI(self, container):
        layout = QVBoxLayout()
        content_widget = QWidget()
        self.scroll_area.setWidget(content_widget)
        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setHorizontalScrollBarPolicy(False)  # ScrollBarAlwaysOff

        scroll_layout = QVBoxLayout()
        content_widget.setLayout(scroll_layout)

        # Ajoutez des images à la liste
        for items_class in Loot.__subclasses__():
            for _ in range(100):
                pixmap = QPixmap(items_class.getDefaultTexturePath())
                pixmap.scaled(2048, 2048)
                label = QLabel()
                label.setPixmap(pixmap)
                scroll_layout.addWidget(label)

        layout.addWidget(self.scroll_area)
        self.setLayout(layout)
        container.setLayout(layout)
