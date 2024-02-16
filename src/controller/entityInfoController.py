from PyQt6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QLabel

from model.entities.entity import Entity
from view.entityInfoView import EntityInfoView
from model.entityInfoModel import EntityInfoModel


class EntityInfoController:
    def __init__(self, dock):
        self.entity = None
        self.view = EntityInfoView(dock)
        self.initialize()

    def initialize(self):
        self.view.initialize()

    def update(self):
        self.view.updateOnStep()

    def setEntity(self, entity: Entity):
        self.entity = entity
        self.view.setEntity(entity)
