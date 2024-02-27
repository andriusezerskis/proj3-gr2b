from abc import abstractmethod

from utils import Point


class Movable:

    @abstractmethod
    def getPos(self) -> Point:
        ...
