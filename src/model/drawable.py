"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""


from abc import ABC, abstractmethod
from utils import getTerminalSubclassesOfClass
from typing import Any
from json import load
from random import choice


class ParametrizedDrawable(ABC):
    parameterDicts: dict = dict()

    @classmethod
    def _getParameters(cls) -> dict:
        if cls not in cls.parameterDicts.keys():
            with open(cls._getConfigFilePath(), "r") as f:
                cls.parameterDicts[cls] = load(f)

        return cls.parameterDicts[cls]

    @classmethod
    def reloadAllDicts(cls):
        cls.parameterDicts = dict()
        for parameterType in getTerminalSubclassesOfClass(ParametrizedDrawable):
            parameterType._getParameters()

    @classmethod
    @abstractmethod
    def _getConfigFilePath(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def _getFilePathPrefix(cls) -> str:
        ...

    @classmethod
    def getParameters(cls) -> dict:
        assert cls.__name__ in cls._getParameters().keys(), f"{cls.__name__} is not a configured (sub)type"
        return cls._getParameters()[cls.__name__]

    @classmethod
    def _getParameter(cls, parameter: str) -> Any:
        return cls.getParameters()[parameter]

    @classmethod
    def _constructFullTexturePath(cls, suffix: str) -> str:
        return cls._getFilePathPrefix() + "/" + suffix

    @classmethod
    def getDefaultTexturePath(cls) -> str:
        return cls._constructFullTexturePath(cls._getParameter("texture_path")[0])

    @classmethod
    def getIconTexturePath(cls) -> str:
        return cls._constructFullTexturePath(cls._getParameter("icon_texture_path"))

    @classmethod
    def pickRandomTexturePath(cls) -> str:
        return cls._constructFullTexturePath(choice(cls._getParameter("texture_path")))

    def getTexturePath(self) -> str:
        return self._texturePath

    def __init__(self):
        if self.__class__.__name__ == "Player":
            return

        self._texturePath = self.pickRandomTexturePath()
