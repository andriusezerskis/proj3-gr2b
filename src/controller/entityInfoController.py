"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""
from PyQt6.QtWidgets import QWidget
from model.entities.entity import Entity
from view.entityInfoView import EntityInfoView


class EntityInfoController:
    def __init__(self, container: QWidget):
        self.view = EntityInfoView(container)

    def update(self):
        self.view.updateOnStep()

    def setEntity(self, entity: Entity):
        self.view.setEntity(entity)
