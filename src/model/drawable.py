"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""


from abc import ABC, abstractmethod


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
    def getTexturePath(cls) -> str:
        return cls._getFilePathPrefix() + "/" + cls._getParameter("texture_path")
