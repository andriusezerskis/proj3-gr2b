"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC, abstractmethod
from utils import getTerminalSubclassesOfClass


class AutomaticGenerator(ABC):

    @classmethod
    @abstractmethod
    def getBaseClass(cls) -> type:
        ...

    @classmethod
    def getTerminalChildrenOfBaseClass(cls) -> set[type]:
        return getTerminalSubclassesOfClass(cls.getBaseClass())
