from PyQt6.QtWidgets import QMessageBox, QDockWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon


class EntityInfoView(QDockWidget):
    def __init__(self, title: str, mainWindow):
        super().__init__(self, title, mainWindow)
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.messageBox = QLabel()
        
    def initialize(self):
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.layout.addWidget(self.messageBox)
        self.messageBox.setText("No entities selected")
        
        
    def draw_entity_info(self):
        """Shows information about an entity"""
        entity_info = f"Age: {self.entity.getAge()}\nHunger: {self.entity.getHunger()}"
        self.messageBox.setText(entity_info)
        