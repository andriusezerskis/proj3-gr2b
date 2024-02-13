from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QWidget

class EntityInfoModel:
    def __init__(self, entity):
        self.entity = entity
        
    def getEntity(self):
        return self.entity
    
    def setEntity(self, entity):
        self.entity = entity