from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon


class EntityInfoModel:
    def __init__(self, entity):
        self.entity = entity
        self.initial_age = entity.getAge()
        self.initial_hunger = entity.getHunger()
        self.message_box = QMessageBox()

    def draw_entity_info(self):
        entity_info = f"Age: {self.entity.getAge()}\nHunger: {self.entity.getHunger()}"
        self.message_box.setWindowTitle("Entity Information")
        self.message_box.setText(entity_info)
        self.message_box.setWindowIcon(QIcon(self.entity.getTexturePath()))
        self.message_box.exec()
        