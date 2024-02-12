from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QWidget

class EntityInfoModel:
    def __init__(self, entity):
        self.entity = entity
        self.initial_age = entity.getAge()
        self.initial_hunger = entity.getHunger()