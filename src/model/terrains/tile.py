"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC
from typing import TypeVar
from overrides import override


from model.entities.entity import Entity
from model.drawable import ParametrizedDrawable

from utils import Point
from constants import FIRE, ICE, TILE_PARAMETERS, TILES_TEXTURE_FOLDER_PATH, Disaster


Tile_ = TypeVar("Tile_")


class Tile(ParametrizedDrawable, ABC):

    def __init__(self, pos: Point, height: float) -> None:
        super().__init__()
        self.pos = pos
        self.height = height
        self.entity = None
        self.disaster = None
        self.disasterOpacity = 0

    def getDisasterPathName(self):
        if self.disaster == Disaster.FIRE_TEXT:
            return FIRE
        elif self.disaster == Disaster.ICE_TEXT:
            return ICE
        return None

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

    @classmethod
    def isGradientAscending(cls) -> bool:
        return bool(cls._getParameter("ascending_gradient"))

    def getHeight(self) -> float:
        return self.height

    # @abstractmethod
    def step(self):
        pass

    def getEntity(self) -> Entity | None:
        return self.entity

    def hasEntity(self) -> bool:
        return self.entity is not None

    def setEntity(self, entity: Entity) -> bool:
        """
        Sets the entity in the tile
        :param entity: the entity that you want to place
        :return: whether the assignment was successful
        """
        # we only set the entity if the tile is of a valid type
        if entity and entity.isValidTileType(self.__class__):
            self.entity = entity
            return True
        return False
    
    def setDisaster(self, disasterType: str) -> None:
        self.disaster = disasterType

    def setDisasterOpacity(self, disasterOpacity: float) -> None:
        self.disasterOpacity = disasterOpacity

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

    @staticmethod
    def copyWithDifferentTypeOf(toCopy: Tile_, type_: type) -> Tile_:
        """
        Copies the passed tile in a new tile of a different tile.
        Attemps to copy the potential entity but might not succeed.
        :param toCopy: The tile to copy
        :param type_: The type of the new tile
        :return:
        """
        tile = type_(toCopy.pos, toCopy.height)
        tile.setEntity(toCopy.entity)
        return tile

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pos})"

    def __str__(self):
        return f"{self.__class__.__name__[0]}"
