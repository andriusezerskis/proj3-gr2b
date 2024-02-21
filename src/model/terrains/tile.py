"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC
from typing import TypeVar

from model.entities.entity import Entity
from model.drawable import ParametrizedDrawable

from utils import Point
from constants import TILE_PARAMETERS, TILES_TEXTURE_FOLDER_PATH

from overrides import override

Tile_ = TypeVar("Tile_")


class Tile(ParametrizedDrawable, ABC):

    def __init__(self, pos: Point, height: float, entity: Entity = None) -> None:
        self.pos = pos
        self.height = height
        self.entity = None
        self.setEntity(entity)
        self.disaster = None
        self.disasterOpacity = 0

    @classmethod
    @override
    def _getParameters(cls) -> dict:
        return TILE_PARAMETERS

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return TILES_TEXTURE_FOLDER_PATH

    @classmethod
    def getLevel(cls) -> float:
        return cls._getParameter("level")

    @classmethod
    def getFilterColor(cls) -> str:
        return cls._getParameter("filter_color")

    def getHeight(self) -> float:
        return self.height

    # @abstractmethod
    def step(self):
        pass

    def getEntity(self) -> Entity | None:
        return self.entity

    def hasEntity(self) -> bool:
        return self.entity is not None

    def setEntity(self, entity: Entity) -> None:
        # we only set the entity if the tile is of a valid type
        if entity and entity.isValidTileType(self.__class__):
            self.entity = entity

    def addNewEntity(self, entity: type) -> None:
        """
        Places a new entity in this tile
        :param entity: the type of entity that must be created
        """
        if not self.entity:
            self.setEntity(entity(self.getPos()))

    def removeEntity(self) -> None:
        if self.entity:
            self.entity = None

    def getPos(self) -> Point:
        return self.pos

    @property
    def index(self) -> tuple[int, int]:
        return self.getIndex()

    def getIndex(self) -> tuple[int, int]:
        return self.pos.y(), self.pos.x()

    @staticmethod
    def copyWithDifferentTypeOf(toCopy: Tile_, type_: type) -> Tile_:
        return type_(toCopy.pos, toCopy.height, toCopy.entity)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pos})"

    def __str__(self):
        return f"{self.__class__.__name__[0]}"
