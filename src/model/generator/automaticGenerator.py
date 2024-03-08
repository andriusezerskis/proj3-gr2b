"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC, abstractmethod
from typing import Type, TypeVar

from utils import getTerminalSubclassesOfClass


C = TypeVar("C")


class AutomaticGenerator(ABC):

    @classmethod
    @abstractmethod
    def getBaseClass(cls) -> Type[C]:
        ...

    @classmethod
    def getTerminalChildrenOfBaseClass(cls) -> set[Type[C]]:
        return getTerminalSubclassesOfClass(cls.getBaseClass())
