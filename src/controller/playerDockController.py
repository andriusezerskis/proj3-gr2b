"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from view.playerDockView import PlayerDockView


class PlayerDockController:
    """Singleton"""
    instance = None

    def __new__(cls, container):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.view = PlayerDockView(container)
        return cls.instance

    @staticmethod
    def getInstance():
        if PlayerDockController.instance is None:
            raise TypeError
        return PlayerDockController.instance
