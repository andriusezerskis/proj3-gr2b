from abc import abstractmethod, ABC
from typing import Any
from json import load
from utils import getTerminalSubclassesOfClass


class GenericParameters(ABC):

    @classmethod
    @abstractmethod
    def getFileName(cls) -> str:
        ...

    @classmethod
    def getFilePath(cls) -> str:
        return "../config/" + cls.getFileName()

    @staticmethod
    def reloadAllDicts():
        for parameterType in getTerminalSubclassesOfClass(GenericParameters):
            parameterType.reloadDict()

    @classmethod
    def reloadDict(cls) -> None:
        with open(cls.getFilePath(), "r") as f:
            d = load(f)
            for key in d.keys():
                if key in cls.__dict__ and getattr(cls, key) is not None and getattr(cls, key) != d[key]:
                    print("modified attribute", key)
                setattr(cls, key, d[key])

    @classmethod
    def get(cls, parameter: str) -> Any:
        return getattr(cls, parameter)
