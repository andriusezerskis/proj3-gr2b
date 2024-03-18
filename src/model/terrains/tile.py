"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""

from abc import ABC
from typing import Type

from overrides import override


from model.entities.entity import Entity
from model.drawable import ParametrizedDrawable
from model.movable import Movable
from model.disaster import Disaster

from utils import Point

from parameters import TerrainParameters, ViewParameters


class Tile(ParametrizedDrawable, ABC):

    def __init__(self, pos: Point, height: float) -> None:
        super().__init__()
        self.pos = pos
        self.height = height
        self.movable: Movable | None = None
        self.disaster: str | None = None
        self.disasterOpacity = 0
        self.temperature = 0

    def getDisasterPathName(self):
        if self.disaster == Disaster.FIRE_TEXT:
            return ViewParameters.FIRE_TEXTURE_PATH
        elif self.disaster == Disaster.ICE_TEXT:
            return ViewParameters.ICE_TEXTURE_PATH
        return None

    @classmethod
    @override
    def _getConfigFilePath(cls) -> str:
        return "../config/tiles.json"

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return TerrainParameters.TEXTURE_FOLDER_PATH

    @classmethod
    def getLevel(cls) -> float:
        return cls._getParameter("level")

    def updateTemperature(self, temperature: float):
        self.temperature = temperature

    def getTemperature(self) -> float:
        return self.temperature

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

    def getEntity(self) -> Movable | None:
        return self.movable

    def hasEntity(self) -> bool:
        return self.movable is not None

    def setEntity(self, entity: Movable) -> bool:
        """
        Sets the entity in the tile
        :param entity: the entity that you want to place
        :return: whether the assignment was successful
        """
        # we only set the entity if the tile is of a valid type
        if entity and entity.isValidTileType(self.__class__):
            self.movable = entity
            return True
        return False

    def getDisaster(self) -> str:
        return self.disaster

    def setDisaster(self, disasterType: str) -> None:
        self.disaster = disasterType

    def getDisasterOpacity(self) -> float:
        return self.disasterOpacity

    def setDisasterOpacity(self, disasterOpacity: float) -> None:
        self.disasterOpacity = disasterOpacity

    def addNewEntity(self, entity: Type[Entity], age: int = 0) -> None:
        """
        Places a new entity in this tile
        :param entity: the type of entity that must be created
        :param age: the age of the new entity
        """
        if not self.movable and entity and entity.isValidTileType(self.__class__):
            newEntity = entity(self.getPos())
            self.setEntity(newEntity)
            newEntity.setAge(age)

    def removeEntity(self) -> None:
        if self.movable:
            self.movable = None

    def getPos(self) -> Point:
        return self.pos

    @staticmethod
    def copyWithDifferentTypeOf(toCopy: "Tile_", type_: Type["Tile_"]) -> "Tile_":
        """
        Copies the passed tile in a new tile of a different tile.
        Attemps to copy the potential entity but might not succeed.
        :param toCopy: The tile to copy
        :param type_: The type of the new tile
        :return:
        """
        tile = type_(toCopy.pos, toCopy.height)
        tile.setEntity(toCopy.getEntity())
        tile.setDisaster(toCopy.getDisaster())
        tile.setDisasterOpacity(toCopy.getDisasterOpacity())
        return tile

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pos})"

    def __str__(self):
        return f"{self.__class__.__name__[0]}"
