"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""


from abc import ABC, abstractmethod
from random import choice


class ParametrizedDrawable(ABC):

    @classmethod
    @abstractmethod
    def _getParameters(cls) -> dict:
        ...

    @classmethod
    @abstractmethod
    def _getFilePathPrefix(cls) -> str:
        ...

    @classmethod
    def getParameters(cls) -> dict:
        return cls._getParameters()[cls.__name__]

    @classmethod
    def _getParameter(cls, parameter: str) -> list[str] | str | int | float:
        return cls.getParameters()[parameter]

    @classmethod
    def _constructFullTexturePath(cls, suffix: str) -> str:
        return cls._getFilePathPrefix() + "/" + suffix

    @classmethod
    def getDefaultTexturePath(cls) -> str:
        return cls._constructFullTexturePath(cls._getParameter("texture_path")[0])

    @classmethod
    def pickRandomTexturePath(cls) -> str:
        return cls._constructFullTexturePath(choice(cls._getParameter("texture_path")))

    def getTexturePath(self) -> str:
        return self._texture_path

    def __init__(self):
        if self.__class__.__name__ == "Player":
            return

        self._texture_path = self.pickRandomTexturePath()
