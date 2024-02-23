"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from model.entities.entity import Entity
from view.entityInfoView import EntityInfoView


class EntityInfoController:
    def __init__(self, dock, container):
        self.entity = None
        self.view = EntityInfoView(dock, container)
        self.view.initialize()

    def update(self):
        self.view.updateOnStep()

    def setEntity(self, entity: Entity):
        self.entity = entity
        self.view.setEntity(entity)
