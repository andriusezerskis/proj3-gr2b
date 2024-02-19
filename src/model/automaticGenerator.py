"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC, abstractmethod


class AutomaticGenerator(ABC):

    @classmethod
    @abstractmethod
    def getBaseClass(cls) -> type:
        ...

    @classmethod
    def getTerminalChildrenOfBaseClass(cls) -> set[type]:
        res = set()
        stack = [cls.getBaseClass()]
        while len(stack) > 0:
            current = stack.pop()
            subclasses = current.__subclasses__()
            if len(subclasses) == 0:
                res.add(current)
            else:
                stack.extend(subclasses)
        return res
